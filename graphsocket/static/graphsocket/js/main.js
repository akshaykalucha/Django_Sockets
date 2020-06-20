

let ws = new WebSocket('ws://localhost:8000/ws/polData/')

ws.onopen = function (e){
    alert('connection established')
}

ws.onmessage = function (e) {
    console.log(e.data)
    var recvdata = JSON.parse(e.data)
    dataObj = dataObject['data']['datasets'][0]['data']
    dataObj.shift();
    dataObj.push(recvdata.value)
    dataObject['data']['datasets'][0]['data'] = dataObj
    window.myLine.update()
}

ws.onclose = function (e){
    alert('Conn Closed')
}

var dataObject = {
    type: 'line',
    data: {
        labels: [1,2,3,4,5,6],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3]
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
}

var ctx = document.getElementById('myChart').getContext('2d');
window.myLine = new Chart(ctx, dataObject);