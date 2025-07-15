from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            declared_attr,
                            mapped_column
                            )


class Base(DeclarativeBase):
    """
    Заготовка для всех таблиц БД
    с первичным полем 'id'
    """

    __abstract__ = True

    # Автоматом именуем таблицы по названию класса
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
