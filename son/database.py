from datetime import datetime

from alchemical import Model
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Playlist(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    songs: Mapped[list['Song']] = relationship(back_populates='playlist', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'Playlist(id={self.id!r}, name={self.name!r})'


class Song(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True, default=func.now()
    )
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    playlist_id: Mapped[int] = mapped_column(ForeignKey('playlist.id'))
    playlist: Mapped['Playlist'] = relationship(back_populates='songs')

    __table_args__ = (UniqueConstraint('path', 'playlist_id', name='_playlist_song_uc'),)

    def __repr__(self) -> str:
        return f'Song(id={self.id!r}, path={self.path!r})'
