from dataclasses import dataclass


@dataclass
class IOChannel:
    """DI/DO 한 채널의 정보를 담는 단순 데이터 모델입니다."""

    number: int
    name: str
    is_on: bool = False

    @property
    def code(self) -> str:
        return f"{self.number:02d}"
