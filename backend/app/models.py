import enum
from uuid import uuid4
from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, Enum, ForeignKey, CheckConstraint, UniqueConstraint, func, JSON

from sqlalchemy.dialects.postgresql import UUID,ARRAY
from sqlalchemy.orm import relationship
from .db import Base

class ProgramStatus(enum.Enum):
    draft="draft"
    published="published"
    archived="archived"

class Program(Base):
    __tablename__ = "programs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    language_primary = Column(String, nullable=False)
    languages_available=Column(ARRAY(String),nullable=False)
    status = Column(Enum(ProgramStatus,name="program_status"),
                    default=ProgramStatus.draft,
                    nullable=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime,server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "language_primary= ANY(languages_available)",
            name="program_primary_lang_in_available"),
    )

class Topic(Base):
    __tablename__="topics"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False,unique=True)

class ProgramTopic(Base):
    __tablename__="program_topics"
    program_id=Column(UUID(as_uuid=True),ForeignKey("programs.id"),primary_key=True)
    topic_id=Column(Integer,ForeignKey("topics.id"),primary_key=True)

class Term(Base):
    __tablename__="terms"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    program_id=Column(UUID(as_uuid=True),ForeignKey("programs.id"),nullable=False)
    term_number=Column(Integer,nullable=False)
    title=Column(String)
    status = Column(String, nullable=False, default="draft")
    created_at=Column(DateTime,server_default=func.now())
    __table_args__=(
        UniqueConstraint("program_id","term_number",name="uq_program_term"),
    )

class LessonStatus(enum.Enum):
    draft="draft"
    scheduled="scheduled"
    published="published"
    archived="archived"

class ContentType(enum.Enum):
    video="video"
    article="article"
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id"), nullable=False)

    lesson_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)

    content_type = Column(
        Enum("video", "article", name="content_type"),
        nullable=False,
    )

    duration_ms = Column(Integer, nullable=True)
    is_paid = Column(Boolean, nullable=False, default=False)

    content_language_primary = Column(String, nullable=False)
    content_languages_available = Column(ARRAY(String), nullable=False)

    content_urls_by_language = Column(JSON, nullable=False)

    status = Column(
        Enum("draft", "scheduled", "published", "archived", name="lesson_status"),
        nullable=False,
        default="draft",
    )

    publish_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    term = relationship("Term", backref="lessons")

class UserRole(enum.Enum):
    admin="admin"
    editor="editor"
    viewer="viewer"

class User(Base):
    __tablename__="users"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email=Column(String,nullable=False,unique=True)
    password_hash=Column(String,nullable=False)
    role = Column(Enum(UserRole,name="user_role"),nullable=False,default=UserRole.viewer)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,server_default=func.now())

