class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        mess = (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')
        return mess


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        callor = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                   + self.CALORIES_MEAN_SPEED_SHIFT)
                  * self.weight / self.M_IN_KM * self.MIN_IN_H * self.duration)
        return callor


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_1: float = 0.035
    CALORIES_WEIGHT_2: float = 0.029
    SPEED_METERS_PER_SECOND: float = 0.278
    MTR_PER_HEIGHT: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        callor = ((self.CALORIES_WEIGHT_1 * self.weight
                   + ((self.get_mean_speed() * self.SPEED_METERS_PER_SECOND)**2
                       / (self.height / self.MTR_PER_HEIGHT))
                  * self.CALORIES_WEIGHT_2 * self.weight)
                  * self.duration * self.MIN_IN_H)
        return callor


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWM_COEFF: float = 1.1
    WEIGHT_COEFF: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_spd: float = (self.length_pool * self.count_pool / self.M_IN_KM
                           / self.duration)
        return mean_spd

    def get_spent_calories(self) -> float:
        # (средняя_скорость + 1.1) * 2 * вес * время_тренировки
        callor: float = ((self.get_mean_speed() + self.SWM_COEFF)
                         * self.WEIGHT_COEFF * self.weight * self.duration)
        return callor


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    tp_trng = {'SWM': Swimming,
               'RUN': Running,
               'WLK': SportsWalking
               }
    return tp_trng[workout_type](*data)


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
