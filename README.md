# Мессенджер
## Технологии
1. Prometheus, Grafana
2. Python


## Развертывание
1. Клонирование репозитория
```bash
git clone https://github.com/vkkuznetsov/OROPO_lab10.git
cd OROPO_lab10
```

2. Создание виртуального окружения
```bash
python3 -m venv venv
```
3. Активирование венв
```bash
source venv/bin/activate #linux
или
.\venv\Scripts\activate #windows
```
3. Установка зависимостей
```bash
pip install -r req.txt 
```
4. Проверка конфигурации env в терминале  
Программа читает из переменных окружения EXPORTER_HOST , EXPORTER_PORT  
Чтобы их определить нужно выполнить команду  
На windows это делается командой (powershell)
```bash
set EXPORTER_HOST=127.0.0.1
set EXPORTER_PORT=8000
```
На windows (cmd)
```bash
$env:EXPORTER_HOST = "127.0.0.1"
$env:EXPORTER_PORT = "8000"
```
На Linux 
```bash
export EXPORTER_HOST=127.0.0.1
export EXPORTER_PORT=8000
```
Проверка переменных окружения  
Windows  
Powershell
```bash
Write-Host "EXPORTER_HOST: $env:EXPORTER_HOST"
Write-Host "EXPORTER_PORT: $env:EXPORTER_PORT"
```
CMD  
```bash
echo %EXPORTER_HOST%
echo %EXPORTER_PORT%
```
Linux
```bash
echo $EXPORTER_HOST
echo $EXPORTER_PORT
```
ЕСЛИ ОНИ НЕ УСТАНОВЛЕНЫ ТО БУДУТ ИСПОЛЬЗОВАТЬСЯ ЗНАЧЕНИЯ ПО УМОЛЧАНИЮ (127.0.0.1 8080)  
5. Запуск приложения (активированный venv), в консоли покажется хост и порт на котором запустится экспортер
```bash
python main.py
```

## Запросы PromQL
1. Информация про загрузку ЦП
```bash
sum(cpu_usage_percent) by (core)
```
2. Информация про загрузку памяти
```bash
memory_used_bytes or label_replace(memory_total_bytes, "distinct", "total", "__name__", ".*") 
```
3. Информация про память дисков
```bash
disk_used_bytes or label_replace(disk_total_bytes, "distinct", "total", "__name__", ".*") 
```
# Дашборд Grafana 
### Расположен в папке grafana/dashboard.json 

# Для себя
Запуск в докере, у графаны хост нужно указывать host.docker.internal, ну либо сеть им создавать через докер  
Grafana
```bash
docker run -d -p 3000:3000 --name=grafana grafana/grafana
```

Prometheus
```bash
docker run -d --name=prometheus -p 9090:9090 -v ${PWD}/prometheus_data/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```
