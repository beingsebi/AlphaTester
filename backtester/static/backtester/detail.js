const len = dataTimeSeries.length;
let ctxFreeFundsOverTime = document.getElementById('chart_freeFundsOverTime').getContext('2d');
let chartFreeFundsOverTime = new Chart(ctxFreeFundsOverTime, {
    type: 'line',
    data: {
        labels: dataTimeSeries,
        datasets: [{
            label: 'Free Funds Over Time',
            data: dataFreeFundsOverTime
        }]
    },
    options: {
        scales: {
            x: {
                ticks: {
                callback: function(val, index) {
                    return index % Math.floor(len/6) === 0 ? this.getLabelForValue(val) : '';
                },
                }
            }
        }
    }
    });
let ctxBalanceOverTime = document.getElementById('chart_balanceOverTime').getContext('2d');
let chartBalanceOverTime = new Chart(ctxBalanceOverTime, {
    type: 'line',
    data: {
        labels: dataTimeSeries,
        datasets: [{
            label: 'Balance Over Time',
            data: dataBalanceOverTime
        }]
    },
    options: {
        scales: {
            x: {
                ticks: {
                callback: function(val, index) {
                    return index % Math.floor(len/6) === 0 ? this.getLabelForValue(val) : '';
                },
                }
            }
        }
    }
    });