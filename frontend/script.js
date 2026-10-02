let myChart = null;
let isLoading = false;

async function sendQuery() {
    console.log("CLICKED");

    let question = document.getElementById("question").value;

    try {
        let response = await fetch("http://127.0.0.1:5000/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        let result = await response.json();

        console.log("FULL RESPONSE:", result);

        if (result.result) {
            result = result.result;
        }

        // SQL
        let sqlBox = document.getElementById("sqlOutput");
        if (sqlBox) {
            sqlBox.innerText = result.sql;
        }

        // TABLE
        renderTable(result.data);

        // CHART
        if (result.chart) {
            renderChart(result);
        } else {
            document.getElementById("chartCanvas").style.display = "none";

            if (myChart) {
                myChart.destroy();
                myChart = null;
            }
        }

    } catch (error) {
        console.error("FETCH ERROR:", error);
    }
}

function renderTable(data) {
    console.log("MASUK renderTable");
    console.log(data);

    let table = document.getElementById("tableOutput");

    if (!table) {
        console.log("tableOutput tidak ada");
        return;
    }

    if (!data || data.length === 0) {
        table.innerHTML = "<tr><td>Tidak ada data</td></tr>";
        return;
    }

    let headers = Object.keys(data[0]);

    let html = "<tr>";
    headers.forEach(h => {
        html += `<th>${h}</th>`;
    });
    html += "</tr>";

    data.forEach(row => {
        html += "<tr>";
        headers.forEach(h => {
            html += `<td>${row[h]}</td>`;
        });
        html += "</tr>";
    });

    console.log("HTML TABLE:", html);

    table.innerHTML = html;
}

function renderChart(result) {
    let canvas = document.getElementById("chartCanvas");

    if (!canvas) return;

    if (myChart) {
        myChart.destroy();
        myChart = null;
    }

    if (!result.chart || !result.data || result.data.length === 0) {
        canvas.style.display = "none";
        return;
    }

    let keys = Object.keys(result.data[0]);

    if (keys.length !== 2) {
        console.log("Data tidak cocok untuk chart");
        canvas.style.display = "none";
        return;
    }

    canvas.style.display = "block";

    let ctx = canvas.getContext("2d");

    let labels = result.data.map(d => Object.values(d)[0]);
    let values = result.data.map(d => Object.values(d)[1]);

    myChart = new Chart(ctx, {
        type: result.chartType || "bar",
        data: {
            labels,
            datasets: [{
                label: result.chartTitle || "Chart",
                data: values
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    console.log("Chart berhasil dibuat");
}
