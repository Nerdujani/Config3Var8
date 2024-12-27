import pytest

from main import Parser


@pytest.mark.parametrize(
    'arg, expected', [
        ('P{}3', 'Некорректный ввод\n'),
        ('!#$%!!#(&(#', 'Некорректный ввод\n'),
    ]
)
def test_wrong_input(capfd, arg, expected):
    Parser().load_toml(arg)
    out, err = capfd.readouterr()
    assert out == expected


@pytest.mark.parametrize(
    'arg, expected', [
        ('''[data]
value = 42
list = [1, 2, 3]

[data.nested]
sub_value = 99
sub_list = [10, 20, 30]
''', '''dict(
    data = dict(
        value = 42,
        list = ({
            1,
            2,
            3
        }),
        nested = dict(
            sub_value = 99,
            sub_list = ({
                10,
                20,
                30
            })
        )
    )
)
'''),
        ('''[metrics]
count = 100
values = [10, 15, 20, 25, 30]

[metrics.series]
series_value = 50
series_list = [[1, 2], [3, 4], [5, 6]]

[settings]
configuration = 500

[settings.levels]
threshold = 75
limits = [10, 20, 30]

[settings.levels.nested]
nested_value = 33
nested_list = [[100, 200], [300, 400], [500, 600]]
''',
         '''dict(
    metrics = dict(
        count = 100,
        values = ({
            10,
            15,
            20,
            25,
            30
        }),
        series = dict(
            series_value = 50,
            series_list = ({
                ({
                    1,
                    2
                }),
                ({
                    3,
                    4
                }),
                ({
                    5,
                    6
                })
            })
        )
    ),
    settings = dict(
        configuration = 500,
        levels = dict(
            threshold = 75,
            limits = ({
                10,
                20,
                30
            }),
            nested = dict(
                nested_value = 33,
                nested_list = ({
                    ({
                        100,
                        200
                    }),
                    ({
                        300,
                        400
                    }),
                    ({
                        500,
                        600
                    })
                })
            )
        )
    )
)
'''),

        ('''[simulation]
duration = 1000  # Время симуляции в секундах
step_size = 0.01  # Шаг интегрирования

[simulation.environment]
gravity = 9.81
air_density = 1.225
temperature = 298

[simulation.environment.wind]
speed = 10
directions = [0, 90, 180, 270]

[objects]
count = 3

[[objects.object]]
mass = 5.0
initial_velocity = [0, 10, 0]
position = [0, 0, 0]

[[objects.object]]
mass = 2.0
initial_velocity = [5, 0, 0]
position = [10, 0, 0]

[[objects.object]]
mass = 10.0
initial_velocity = [0, -5, 0]
position = [-5, 5, 0]
''',
         '''dict(
    simulation = dict(
        duration = 1000,
        step_size = 0.01,
        environment = dict(
            gravity = 9.81,
            air_density = 1.225,
            temperature = 298,
            wind = dict(
                speed = 10,
                directions = ({
                    0,
                    90,
                    180,
                    270
                })
            )
        )
    ),
    objects = dict(
        count = 3,
        object = ({
            dict(
                mass = 5.0,
                initial_velocity = ({
                    0,
                    10,
                    0
                }),
                position = ({
                    0,
                    0,
                    0
                })
            ),
            dict(
                mass = 2.0,
                initial_velocity = ({
                    5,
                    0,
                    0
                }),
                position = ({
                    10,
                    0,
                    0
                })
            ),
            dict(
                mass = 10.0,
                initial_velocity = ({
                    0,
                    -5,
                    0
                }),
                position = ({
                    -5,
                    5,
                    0
                })
            )
        })
    )
)
'''),
    ]
)
def test_correct_input(arg, expected):
    p = Parser()
    p.rec_parse(p.load_toml(arg), 0)
    assert p.s == expected
