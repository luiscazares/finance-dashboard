let stockChart, cryptoChart;

async function loadStock() {
    const ticker = document.getElementById("stock-input").value.trim();
    const res = await fetch(`/api/stock/${ticker}`);
    const data = await res.json();

    document.getElementById("stock-price").textContent = `Current Price: $${data.current_price}`;
    renderChart("stock-chart", data.history, `${ticker} (1 Month)`, stockChart, c => stockChart = c);
}

async function loadCrypto() {
    const coin = document.getElementById("crypto-input").value.trim();
    const res = await fetch(`/api/crypto/${coin}`);
    const data = await res.json();

    document.getElementById("crypto-price").textContent = `Current Price: $${data.current_price}`;
    renderChart("crypto-chart", data.history, `${coin} (30 Days)`, cryptoChart, c => cryptoChart = c);
}

function renderChart(canvasId, history, label, existingChart, setChart) {
    const labels = history.map(p => p.date);
    const prices = history.map(p => p.close);

    if (existingChart) existingChart.destroy();

    const ctx = document.getElementById(canvasId).getContext("2d");
    setChart(new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [{ label, data: prices, borderColor: "#4f8ef7", fill: false }]
        },
        options: { responsive: true }
    }));
}
