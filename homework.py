from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        mess = (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')
        return mess


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_spd: float = self.get_distance() / self.duration
        return mean_spd

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
              'get_spent_calories() не определена в классе'
              '%s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        callor = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                   + self.CALORIES_MEAN_SPEED_SHIFT)
                  * self.weight / self.M_IN_KM * self.MIN_IN_H * self.duration)
        return callor


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: int

    CALORIES_WEIGHT_1: ClassVar[float] = 0.035
    CALORIES_WEIGHT_2: ClassVar[float] = 0.029
    SPEED_METERS_PER_SECOND: ClassVar[float] = 0.278
    MTR_PER_HEIGHT: ClassVar[int] = 100

    def get_spent_calories(self) -> float:
        callor = ((self.CALORIES_WEIGHT_1 * self.weight
                   + ((self.get_mean_speed() * self.SPEED_METERS_PER_SECOND)**2
                       / (self.height / self.MTR_PER_HEIGHT))
                  * self.CALORIES_WEIGHT_2 * self.weight)
                  * self.duration * self.MIN_IN_H)
        return callor


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int

    LEN_STEP: ClassVar[float] = 1.38
    SWM_COEFF: ClassVar[float] = 1.1
    WEIGHT_COEFF: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_spd: float = (self.length_pool * self.count_pool / self.M_IN_KM
                           / self.duration)
        return mean_spd

    def get_spent_calories(self) -> float:
        callor: float = ((self.get_mean_speed() + self.SWM_COEFF)
                         * self.WEIGHT_COEFF * self.weight * self.duration)
        return callor


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    tp_trng: dict[str, Training] = {'SWM': Swimming,
                                    'RUN': Running,
                                    'WLK': SportsWalking
                                    }
    if workout_type in tp_trng:
        tp_class: Training = tp_trng[workout_type](*data)
        return tp_class
    raise KeyError(f'Тип тренировки: {workout_type} отсутсвует')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
