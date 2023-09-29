from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращает сообщение о тренировке."""

        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000.0
    H_IN_M = 60.0

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Метод обязательный_метод должен быть '
            f'реализован в подклассе {self.__class__.__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18.0
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.H_IN_M
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KMH_IN_MS = 0.278
    WEIGHT_MULTIPLIER = 0.035
    AVER_SPEED_CALORIE = 0.029
    SM_IN_M = 100.0

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed_ms = self.get_mean_speed() * self.KMH_IN_MS
        return (
            (
                self.WEIGHT_MULTIPLIER * self.weight
                + (mean_speed_ms**2 / (self.height / self.SM_IN_M))
                * self.AVER_SPEED_CALORIE
                * self.weight
            )
            * self.duration
            * self.H_IN_M
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    MEAN_SPEED_SHIFT = 1.1
    SPEED_MULTIPLIER = 2.0

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.MEAN_SPEED_SHIFT)
            * self.SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: dict[str, type[Training]] = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking,
    }
    if workout_type not in training_types:
        workout_list = ', '.join(training_types)
        raise ValueError(
            f'Тренировки вида {workout_type} не найдено. '
            f'Список тренировок: {workout_list}.'
        )
    training_class = training_types[workout_type]
    return training_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
