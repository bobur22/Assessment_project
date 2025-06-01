fetch('/api/chart-data/')
  .then(res => res.json())
  .then(data => {
    var ctx = document.getElementById("myBarChart");
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.bar.labels,
        datasets: [{
          label: "Revenue",
          backgroundColor: "#4e73df",
          hoverBackgroundColor: "#2e59d9",
          borderColor: "#4e73df",
          data: data.bar.data,
        }],
      },
      options: {
        maintainAspectRatio: false,
        layout: {
          padding: { left: 10, right: 25, top: 25, bottom: 0 }
        },
        scales: {
          xAxes: [{
            time: { unit: 'month' },
            gridLines: { display: false, drawBorder: false },
            ticks: { maxTicksLimit: 6 },
            maxBarThickness: 25,
          }],
          yAxes: [{
            ticks: {
              min: 0,
              max: 15000,
              maxTicksLimit: 5,
              padding: 10,
              callback: function(value) {
                return '$' + number_format(value);
              }
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
        legend: { display: false },
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          caretPadding: 10,
          callbacks: {
            label: function(tooltipItem, chart) {
              var label = chart.datasets[tooltipItem.datasetIndex].label || '';
              return label + ': $' + number_format(tooltipItem.yLabel);
            }
          }
        },
      }
    });
  });
