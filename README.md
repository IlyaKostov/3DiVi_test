Версия Python 3.12  
Используется брокер сообщений RabbitMQ

# Запуск
Установить и активировать виртуальное окружение:  
`python -m venv venv`  
`venv/bin/activate`  
Выполнить команду для установки зависимостей: `pip install -r requirements.txt`

Последовательный запуск сервисов

Приемщик
`python -m receiver_service/receiver.py`;

Обработчик
`python -m processor_service/processor.py`;

Запись
`python -m writer_service/writer.py`;

Клиент
`python -m client_service/client.py`;


# Запуск в докер

Для запуска необходимо выполнить 4 команды для сборки образов:

`docker build -t receiver ./receiver_service`  
`docker build -t writer ./writer_service`  
`docker build -t processor ./processor_service`  
`docker build -t client ./client_service`  

Запустить контейнеры:

`docker run receiver`  
`docker run writer`  
`docker run processor`  
`docker run client`


Используя docker-compose
`docker-compose up --build`


P.S.: 
Запуск через Докер полноценно не работает, возникли проблемы с библиотекой pika. 
Сделал как понял задание. Вероятнее всего решение не правильное. Есть еще над чем подумать.
До этого с асинхронкой не сталкивался, как и с RabiitMQ.
