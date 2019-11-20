## 11/20/2019
## Ma Yingxue
## 对海口市半年的滴滴订单数量进行时间序列分析并用前5个月的数据预测最后一个月的数据
library("zoo")
library("forecast")
file <- 'D:/CCF2019/codes/data_dayly_count.csv'
order_num <- read.table(file,sep=',', header=1)
order_num

order_ls <- order_num[2]
orders <- ts(order_ls, start=1, frequency = 7)
plot.ts(orders)
orders

orders_log <- log(orders)
order_diff <- diff(orders_log, differences = 1)
plot.ts(order_diff)

acf(order_diff, lag.max = 30)
acf(order_diff, lag.max=30, plot=FALSE)

pacf(order_diff, lag.max = 30)
pacf(order_diff, lag.max=30, plot=FALSE)

auto.arima(orders_log, trace=T)

arima_model <- arima(orders_log, order=c(2,0,2), seasonal = list(order=c(0,1,2), period=7),method = "ML")
arima_model

order_forecast <- forecast(arima_model, h=31, level=c(99.5))
order_forecast
plot.forecast(order_forecast)
