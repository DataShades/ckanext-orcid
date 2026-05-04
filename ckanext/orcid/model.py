from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy.orm import Mapped

import ckan.plugins.toolkit as tk
from ckan import model


def _current_datetime():
    return datetime.now(tz=timezone.utc)


class OrcidUserLink(tk.BaseModel):
    __table__ = sa.Table(
        "orcid_user_link",
        tk.BaseModel.metadata,
        sa.Column("orcid_id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey('user.id'), nullable=False),
        sa.Column("access_token", sa.String, nullable=False),
        sa.Column("created", sa.DateTime, default=_current_datetime),
    )

    orcid_id: Mapped[str]
    user_id: Mapped[str]
    access_token: Mapped[str]
    created: Mapped[datetime]

    @classmethod
    def get(cls, user_id: str) -> "OrcidUserLink | None":
        return (
            model.Session.query(cls)
            .filter_by(user_id=user_id)
            .first()
        )

    @classmethod
    def add(cls, orcid_id: str, user_id: str, access_token: str) -> "OrcidUserLink":
        link = cls(orcid_id=orcid_id, user_id=user_id, access_token=access_token)
        model.Session.add(link)
        model.Session.commit()
        return link
