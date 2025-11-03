"""
Cache Manager for YouTube Video Analysis
Multi-layer caching system to avoid redundant downloads, transcriptions, and embeddings.

Cache Structure:
.cache/
├── transcripts/VIDEO_ID.txt
├── embeddings/VIDEO_ID_embeddings.pkl
├── frames/VIDEO_ID/frame_*.jpg
└── analysis/VIDEO_ID_analysis.json

Features:
- TTL support for analysis cache
- Cache hit/miss tracking
- Automatic cache directory creation
- Cache validation
- Statistics tracking
"""

import os
import json
import pickle
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class CacheStats:
    """Cache statistics"""
    total_requests: int = 0
    transcript_hits: int = 0
    transcript_misses: int = 0
    embedding_hits: int = 0
    embedding_misses: int = 0
    frame_hits: int = 0
    frame_misses: int = 0
    analysis_hits: int = 0
    analysis_misses: int = 0
    bytes_saved: int = 0

    @property
    def total_hits(self) -> int:
        return (self.transcript_hits + self.embedding_hits +
                self.frame_hits + self.analysis_hits)

    @property
    def total_misses(self) -> int:
        return (self.transcript_misses + self.embedding_misses +
                self.frame_misses + self.analysis_misses)

    @property
    def hit_rate(self) -> float:
        total = self.total_hits + self.total_misses
        return (self.total_hits / total * 100) if total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CacheManager:
    """
    Multi-layer cache manager for YouTube video analysis

    Features:
    - Separate caches for transcripts, embeddings, frames, analysis
    - TTL support for time-sensitive data
    - Cache statistics tracking
    - Automatic cleanup and validation
    """

    DEFAULT_TTL_HOURS = 168  # 7 days for analysis cache

    def __init__(self, cache_dir: str = ".cache", ttl_hours: Optional[int] = None):
        """
        Initialize cache manager

        Args:
            cache_dir: Root cache directory
            ttl_hours: Time-to-live for analysis cache in hours
        """
        self.cache_dir = Path(cache_dir)
        self.ttl_hours = ttl_hours or self.DEFAULT_TTL_HOURS
        self.stats = CacheStats()

        # Create cache subdirectories
        self.transcript_dir = self.cache_dir / "transcripts"
        self.embedding_dir = self.cache_dir / "embeddings"
        self.frame_dir = self.cache_dir / "frames"
        self.analysis_dir = self.cache_dir / "analysis"

        # Create directories
        for dir_path in [self.transcript_dir, self.embedding_dir,
                         self.frame_dir, self.analysis_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Load or initialize stats
        self._load_stats()

    def _load_stats(self):
        """Load cache statistics from disk"""
        stats_file = self.cache_dir / "cache_stats.json"
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                    self.stats = CacheStats(**data)
            except Exception as e:
                print(f"[WARN] Could not load cache stats: {e}")

    def _save_stats(self):
        """Save cache statistics to disk"""
        stats_file = self.cache_dir / "cache_stats.json"
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats.to_dict(), f, indent=2)
        except Exception as e:
            print(f"[WARN] Could not save cache stats: {e}")

    @staticmethod
    def extract_video_id(url: str) -> str:
        """
        Extract video ID from YouTube URL

        Args:
            url: YouTube URL

        Returns:
            Video ID
        """
        # Handle various YouTube URL formats
        if 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        elif 'watch?v=' in url:
            return url.split('watch?v=')[-1].split('&')[0]
        elif 'youtube.com/embed/' in url:
            return url.split('embed/')[-1].split('?')[0]
        else:
            # Assume it's already a video ID
            return url

    def get_transcript_path(self, video_id: str) -> Path:
        """Get path to cached transcript"""
        return self.transcript_dir / f"{video_id}.txt"

    def get_embedding_path(self, video_id: str) -> Path:
        """Get path to cached embeddings"""
        return self.embedding_dir / f"{video_id}_embeddings.pkl"

    def get_frame_dir(self, video_id: str) -> Path:
        """Get directory for cached frames"""
        return self.frame_dir / video_id

    def get_analysis_path(self, video_id: str) -> Path:
        """Get path to cached analysis"""
        return self.analysis_dir / f"{video_id}_analysis.json"

    # Transcript Cache
    def has_transcript(self, video_id: str) -> bool:
        """Check if transcript is cached"""
        path = self.get_transcript_path(video_id)
        exists = path.exists() and path.stat().st_size > 0

        if exists:
            self.stats.transcript_hits += 1
        else:
            self.stats.transcript_misses += 1

        self._save_stats()
        return exists

    def get_transcript(self, video_id: str) -> Optional[str]:
        """Get cached transcript"""
        if not self.has_transcript(video_id):
            return None

        try:
            path = self.get_transcript_path(video_id)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Track bytes saved
            self.stats.bytes_saved += path.stat().st_size
            self._save_stats()

            return content
        except Exception as e:
            print(f"[WARN] Could not read transcript cache: {e}")
            return None

    def save_transcript(self, video_id: str, transcript: str) -> bool:
        """Save transcript to cache"""
        try:
            path = self.get_transcript_path(video_id)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            return True
        except Exception as e:
            print(f"[ERROR] Could not save transcript to cache: {e}")
            return False

    # Embedding Cache
    def has_embeddings(self, video_id: str) -> bool:
        """Check if embeddings are cached"""
        path = self.get_embedding_path(video_id)
        exists = path.exists() and path.stat().st_size > 0

        if exists:
            self.stats.embedding_hits += 1
        else:
            self.stats.embedding_misses += 1

        self._save_stats()
        return exists

    def get_embeddings(self, video_id: str) -> Optional[List[Any]]:
        """Get cached embeddings"""
        if not self.has_embeddings(video_id):
            return None

        try:
            path = self.get_embedding_path(video_id)
            with open(path, 'rb') as f:
                embeddings = pickle.load(f)

            # Track bytes saved
            self.stats.bytes_saved += path.stat().st_size
            self._save_stats()

            return embeddings
        except Exception as e:
            print(f"[WARN] Could not read embedding cache: {e}")
            return None

    def save_embeddings(self, video_id: str, embeddings: List[Any]) -> bool:
        """Save embeddings to cache"""
        try:
            path = self.get_embedding_path(video_id)
            with open(path, 'wb') as f:
                pickle.dump(embeddings, f)
            return True
        except Exception as e:
            print(f"[ERROR] Could not save embeddings to cache: {e}")
            return False

    # Frame Cache
    def has_frames(self, video_id: str) -> bool:
        """Check if frames are cached"""
        frame_dir = self.get_frame_dir(video_id)
        exists = frame_dir.exists() and len(list(frame_dir.glob("*.jpg"))) > 0

        if exists:
            self.stats.frame_hits += 1
        else:
            self.stats.frame_misses += 1

        self._save_stats()
        return exists

    def get_frame_paths(self, video_id: str) -> List[Path]:
        """Get paths to cached frames"""
        if not self.has_frames(video_id):
            return []

        frame_dir = self.get_frame_dir(video_id)
        frames = sorted(frame_dir.glob("*.jpg"))

        # Track bytes saved
        for frame in frames:
            self.stats.bytes_saved += frame.stat().st_size
        self._save_stats()

        return frames

    def save_frame_dir(self, video_id: str, source_dir: Path) -> bool:
        """Copy frames from source directory to cache"""
        try:
            dest_dir = self.get_frame_dir(video_id)

            # Remove existing cache if present
            if dest_dir.exists():
                shutil.rmtree(dest_dir)

            # Copy directory
            shutil.copytree(source_dir, dest_dir)
            return True
        except Exception as e:
            print(f"[ERROR] Could not save frames to cache: {e}")
            return False

    # Analysis Cache (with TTL)
    def has_analysis(self, video_id: str, check_ttl: bool = True) -> bool:
        """
        Check if analysis is cached and not expired

        Args:
            video_id: Video ID
            check_ttl: Whether to check TTL expiration
        """
        path = self.get_analysis_path(video_id)

        if not path.exists():
            self.stats.analysis_misses += 1
            self._save_stats()
            return False

        # Check TTL
        if check_ttl:
            file_age = datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)
            if file_age > timedelta(hours=self.ttl_hours):
                self.stats.analysis_misses += 1
                self._save_stats()
                return False

        self.stats.analysis_hits += 1
        self._save_stats()
        return True

    def get_analysis(self, video_id: str, check_ttl: bool = True) -> Optional[Dict[str, Any]]:
        """Get cached analysis"""
        if not self.has_analysis(video_id, check_ttl):
            return None

        try:
            path = self.get_analysis_path(video_id)
            with open(path, 'r', encoding='utf-8') as f:
                analysis = json.load(f)

            # Track bytes saved
            self.stats.bytes_saved += path.stat().st_size
            self._save_stats()

            return analysis
        except Exception as e:
            print(f"[WARN] Could not read analysis cache: {e}")
            return None

    def save_analysis(self, video_id: str, analysis: Dict[str, Any]) -> bool:
        """Save analysis to cache with timestamp"""
        try:
            # Add cache metadata
            cache_data = {
                'cached_at': datetime.now().isoformat(),
                'ttl_hours': self.ttl_hours,
                'analysis': analysis
            }

            path = self.get_analysis_path(video_id)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            return True
        except Exception as e:
            print(f"[ERROR] Could not save analysis to cache: {e}")
            return False

    # Cache Management
    def clear_all(self) -> int:
        """Clear all caches and return number of files deleted"""
        deleted = 0

        for cache_type in [self.transcript_dir, self.embedding_dir,
                          self.frame_dir, self.analysis_dir]:
            if cache_type.exists():
                for item in cache_type.iterdir():
                    try:
                        if item.is_file():
                            item.unlink()
                            deleted += 1
                        elif item.is_dir():
                            shutil.rmtree(item)
                            deleted += 1
                    except Exception as e:
                        print(f"[WARN] Could not delete {item}: {e}")

        # Reset stats
        self.stats = CacheStats()
        self._save_stats()

        return deleted

    def clear_video(self, video_id: str) -> int:
        """Clear cache for specific video"""
        deleted = 0

        # Transcript
        transcript_path = self.get_transcript_path(video_id)
        if transcript_path.exists():
            transcript_path.unlink()
            deleted += 1

        # Embeddings
        embedding_path = self.get_embedding_path(video_id)
        if embedding_path.exists():
            embedding_path.unlink()
            deleted += 1

        # Frames
        frame_dir = self.get_frame_dir(video_id)
        if frame_dir.exists():
            shutil.rmtree(frame_dir)
            deleted += 1

        # Analysis
        analysis_path = self.get_analysis_path(video_id)
        if analysis_path.exists():
            analysis_path.unlink()
            deleted += 1

        return deleted

    def prune_expired(self) -> int:
        """Remove expired analysis cache entries"""
        deleted = 0

        if not self.analysis_dir.exists():
            return 0

        for analysis_file in self.analysis_dir.glob("*.json"):
            try:
                file_age = datetime.now() - datetime.fromtimestamp(analysis_file.stat().st_mtime)
                if file_age > timedelta(hours=self.ttl_hours):
                    analysis_file.unlink()
                    deleted += 1
            except Exception as e:
                print(f"[WARN] Could not prune {analysis_file}: {e}")

        return deleted

    def validate_cache(self) -> Dict[str, Any]:
        """
        Validate cache integrity and return report

        Returns:
            Dictionary with validation results
        """
        report = {
            'valid': True,
            'transcripts': {'count': 0, 'invalid': []},
            'embeddings': {'count': 0, 'invalid': []},
            'frames': {'count': 0, 'invalid': []},
            'analysis': {'count': 0, 'invalid': [], 'expired': []}
        }

        # Validate transcripts
        for transcript_file in self.transcript_dir.glob("*.txt"):
            report['transcripts']['count'] += 1
            if transcript_file.stat().st_size == 0:
                report['transcripts']['invalid'].append(str(transcript_file))
                report['valid'] = False

        # Validate embeddings
        for embedding_file in self.embedding_dir.glob("*.pkl"):
            report['embeddings']['count'] += 1
            try:
                with open(embedding_file, 'rb') as f:
                    pickle.load(f)
            except Exception:
                report['embeddings']['invalid'].append(str(embedding_file))
                report['valid'] = False

        # Validate frames
        for frame_dir in self.frame_dir.iterdir():
            if frame_dir.is_dir():
                report['frames']['count'] += 1
                if len(list(frame_dir.glob("*.jpg"))) == 0:
                    report['frames']['invalid'].append(str(frame_dir))
                    report['valid'] = False

        # Validate analysis
        for analysis_file in self.analysis_dir.glob("*.json"):
            report['analysis']['count'] += 1
            try:
                with open(analysis_file, 'r') as f:
                    json.load(f)

                # Check expiration
                file_age = datetime.now() - datetime.fromtimestamp(analysis_file.stat().st_mtime)
                if file_age > timedelta(hours=self.ttl_hours):
                    report['analysis']['expired'].append(str(analysis_file))
            except Exception:
                report['analysis']['invalid'].append(str(analysis_file))
                report['valid'] = False

        return report

    def get_cache_size(self) -> Dict[str, int]:
        """Get cache size by category in bytes"""
        sizes = {
            'transcripts': 0,
            'embeddings': 0,
            'frames': 0,
            'analysis': 0,
            'total': 0
        }

        for cache_type, dir_path in [
            ('transcripts', self.transcript_dir),
            ('embeddings', self.embedding_dir),
            ('frames', self.frame_dir),
            ('analysis', self.analysis_dir)
        ]:
            if dir_path.exists():
                for item in dir_path.rglob("*"):
                    if item.is_file():
                        sizes[cache_type] += item.stat().st_size

        sizes['total'] = sum(v for k, v in sizes.items() if k != 'total')
        return sizes

    def print_stats(self):
        """Print cache statistics"""
        print("\n" + "=" * 80)
        print("CACHE STATISTICS")
        print("=" * 80)
        print()

        # Hit rates
        print("Hit Rates:")
        print(f"  Overall: {self.stats.hit_rate:.1f}% ({self.stats.total_hits}/{self.stats.total_hits + self.stats.total_misses})")

        if self.stats.transcript_hits + self.stats.transcript_misses > 0:
            rate = self.stats.transcript_hits / (self.stats.transcript_hits + self.stats.transcript_misses) * 100
            print(f"  Transcripts: {rate:.1f}% ({self.stats.transcript_hits}/{self.stats.transcript_hits + self.stats.transcript_misses})")

        if self.stats.embedding_hits + self.stats.embedding_misses > 0:
            rate = self.stats.embedding_hits / (self.stats.embedding_hits + self.stats.embedding_misses) * 100
            print(f"  Embeddings: {rate:.1f}% ({self.stats.embedding_hits}/{self.stats.embedding_hits + self.stats.embedding_misses})")

        if self.stats.frame_hits + self.stats.frame_misses > 0:
            rate = self.stats.frame_hits / (self.stats.frame_hits + self.stats.frame_misses) * 100
            print(f"  Frames: {rate:.1f}% ({self.stats.frame_hits}/{self.stats.frame_hits + self.stats.frame_misses})")

        if self.stats.analysis_hits + self.stats.analysis_misses > 0:
            rate = self.stats.analysis_hits / (self.stats.analysis_hits + self.stats.analysis_misses) * 100
            print(f"  Analysis: {rate:.1f}% ({self.stats.analysis_hits}/{self.stats.analysis_hits + self.stats.analysis_misses})")

        print()

        # Cache sizes
        sizes = self.get_cache_size()
        print("Cache Sizes:")
        for category, size in sizes.items():
            if category != 'total':
                print(f"  {category.capitalize()}: {size / 1024 / 1024:.2f} MB")
        print(f"  TOTAL: {sizes['total'] / 1024 / 1024:.2f} MB")
        print()

        # Bytes saved
        print(f"Data Transfer Saved: {self.stats.bytes_saved / 1024 / 1024:.2f} MB")
        print()


# Convenience function
_default_cache_manager = None

def get_cache_manager(cache_dir: str = ".cache") -> CacheManager:
    """Get or create default cache manager instance"""
    global _default_cache_manager
    if _default_cache_manager is None:
        _default_cache_manager = CacheManager(cache_dir)
    return _default_cache_manager
