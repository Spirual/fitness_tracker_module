class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
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
    M_IN_KM = 1_000
    H_IN_M = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Метод обязательный_метод должен быть реализован в подклассе'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )
        return info


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        calories = (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.H_IN_M
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KMH_IN_MS = 0.278
    WEIGHT_MULTIPLIER = 0.035
    K1 = 0.029
    SM_IN_M = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: int,
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed() * self.KMH_IN_MS
        calories = (
            (
                self.WEIGHT_MULTIPLIER * self.weight
                + (mean_speed**2 / (self.height / self.SM_IN_M))
                * self.K1
                * self.weight
            )
            * self.duration
            * self.H_IN_M
        )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    MEAN_SPEED_SHIFT = 1.1
    SPEED_MULTIPLIER = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        spent_calories = (
            (mean_speed + self.MEAN_SPEED_SHIFT)
            * self.SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking,
    }
    training_class = training_types[workout_type]
    training = training_class(*data)
    return training


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
