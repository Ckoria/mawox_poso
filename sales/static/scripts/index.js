// -------------- DATA FROM THE DATABASE ------------
  
  //-------------------------------------------------------------
  let accCounts = {
    series: [{
    colors: '#9C27B0',
    name: 'Inflation',
    data: recent_accounts
  }],
    chart: {
    height: 460,
    type: 'bar',
  },
  plotOptions: {
    bar: {
      borderRadius: 10,
      dataLabels: {
        position: 'top', // top, center, bottom
      },
    }
  },
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      return val;
    },
    offsetY: -20,
    style: {
      fontSize: '12px',
      colors: ["#304758"]
    }
  },
  xaxis: {
    categories: past_months,
    position: 'top',
    axisBorder: {
      show: true
    },
    axisTicks: {
      show: true
    },
    crosshairs: {
      show: true,
      fill: {
        type: 'gradient',
        gradient: {
          colorFrom: '#D8E',
          colorTo: '#BED100',
          stops: [0, 100],
          opacityFrom: 0.4,
          opacityTo: 0.5,
        }
      }
    },
    tooltip: {
      enabled: true,
    }
  },
  yaxis: {
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false,
    },
    labels: {
      show: false,
      formatter: function (val) {
        return val;
      }
    }
  },
  title: {
    text: 'No. of Accounts Created in the Past 6 Months',
    floating: true,
    offsetY: 440,
    align: 'center',
    style: {
      color: '#f15'
    }
  }
  };
let chart_s = new ApexCharts(document.querySelector(".chart-sales"), accCounts);
chart_s.render();

//-------------------- SALES OVERVIEW ------------------//

let chart_xpenses = {
  series: [{
  name: past_months[0],
  data: qty[0]
}, {
  name: past_months[1],
  data: qty[1]
}, {
  name: past_months[2],
  data: qty[2]
}, {
  name: past_months[3],
  data: qty[3]
}, {
  name: past_months[4],
  data: qty[4]
}, {
  name: past_months[5],
  data: qty[5]
}],
  chart: {
  type: 'bar',
  height: 500,
  stacked: true,
  stackType: '100%'
},
plotOptions: {
  bar: {
    horizontal: true,
    dataLabels: {
      total: {
        enabled: true,
        offsetX: 1,
        style: {
          fontSize: '14px',
          fontWeight: 600
        }
      }
    }
  },
},
stroke: {
  width: -1,
  colors: ['#ff0']
},
title: {
  text: 'Number of Products Sold in the Past 6 Months',
  align: 'center',
  colors: ['#f15']
},
xaxis: {
  categories: list_of_items
},
yaxis: {
  title: {
    text: ''
  }
},
tooltip: {
  y: {
    formatter: function (val) {
      return val 
    }
  }
},
fill: {
  opacity: 1
},
legend: {
  position: 'bottom',
  horizontalAlign: 'center',
  offsetX: 0
}
};
var chart_x = new ApexCharts(document.querySelector(".chart-xpenses"), chart_xpenses);
chart_x.render();
