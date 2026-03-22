let stockChart, cryptoChart;

async function loadStock(period = "1mo") {
    const inputElement = document.getElementById("stock-input");
    const priceElement = document.getElementById("stock-price");
    const ticker = inputElement.value.trim().toUpperCase();

    if (!ticker) return;

    priceElement.textContent = "Loading...";

    try {
        const res = await fetch(`/api/stock/${ticker}?period=${period}`);
        const stockData = await res.json(); 

        if (!res.ok) throw new Error(stockData.detail || "Failed to fetch data");

        priceElement.textContent = `$${stockData.current_price.toLocaleString()}`;

        renderChart(
            "stock-chart", 
            stockData.history, 
            `${ticker} (${period})`, 
            stockChart, 
            c => stockChart = c
        );
    } catch (err) {
        console.error("Stock Load Error:", err);
        priceElement.textContent = err.message || "Symbol not found";
    }
}

async function loadCrypto(period = "30") {
    const inputElement = document.getElementById("crypto-input");
    const priceElement = document.getElementById("crypto-price");
    const coin = inputElement.value.trim().toLowerCase();
    
    if (!coin) return;

    priceElement.textContent = "Loading...";

    try {
        const res = await fetch(`/api/crypto/${coin}?period=${period}`);
        const cryptoData = await res.json();

        if (!res.ok) throw new Error(cryptoData.detail || "Coin not found");

        const price = cryptoData.current_price;
        if (price == null) throw new Error("No price data available for this coin");
        
        const displayPrice = price < 1 ? price.toFixed(6) : price.toLocaleString();
        priceElement.textContent = `$${displayPrice}`;

        renderChart(
            "crypto-chart", 
            cryptoData.history, 
            `${coin.toUpperCase()} (${period} Days)`, 
            cryptoChart, 
            c => cryptoChart = c
        );
        
    } catch (err) {
        console.error("Crypto Load Error:", err);
        priceElement.textContent = err.message || "Invalid coin";
        if (cryptoChart) {
            cryptoChart.destroy();
            cryptoChart = null;
        }
    }
}

function renderChart(canvasId, history, label, existingChart, setChart) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !history) return;

    const labels = history.map(p => p.date);
    const prices = history.map(p => p.close);

    if (existingChart) {
        existingChart.destroy();
    }

    const ctx = canvas.getContext("2d");
    canvas.style.height = '300px';

    const newChart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [{ 
                label, 
                data: prices, 
                borderColor: "#0dcaf0", 
                backgroundColor: "rgba(13, 202, 240, 0.1)", 
                fill: true,
                tension: 0.3 
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: '#333' },
                    ticks: {
                        color: '#888',
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 8,
                        callback: function(val, index) {
                            const dateStr = this.getLabelForValue(val);
                            const date = !isNaN(dateStr) 
                                ? new Date(parseInt(dateStr) * 1000) 
                                : new Date(dateStr);

                            return date.toLocaleDateString('en-US', { 
                                month: 'short', 
                                day: 'numeric' 
                            });
                        }
                    }
                },
                y: {
                    grid: { color: '#333' },
                    ticks: { color: '#888' }
                }
            },
            plugins: {
                legend: { labels: { color: '#fff' } }
            }
        }
    });
    
    setChart(newChart);
}

const dateEl = document.getElementById("live-date");
if(dateEl) {
    dateEl.textContent = new Date().toLocaleDateString("en-US", { 
        weekday: "short", 
        year: "numeric", 
        month: "short", 
        day: "numeric" 
    });
}