// Chart initialization
const ctx = document.getElementById("myChart");

if (ctx) {
    const myChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            datasets: [{
                data: [0, 100],
                backgroundColor: [
                    "rgb(54, 162, 235)",
                    "rgb(230, 230, 230)"
                ],
                borderWidth: 0
            }]
        },
        options: {
            cutout: "60%",
            plugins: {
                legend: {
                    position: "top"
                }
            }
        }
    });

    function calculateProductivity() {
        let total = 0;
        let completed = 0;

        document.querySelectorAll("#tasklist li").forEach(li => {
            const points = Number(li.dataset.points);
            total += points;

            const checkbox = li.querySelector(".task-checkbox");
            if (checkbox && checkbox.checked) {
                completed += points;
            }
        });

        if (total === 0) return 0;
        return ((completed / total) * 100).toFixed(1);
    }

    function updateChart() {
        const productivity = calculateProductivity();

        myChart.data.datasets[0].data = [
            productivity,
            100 - productivity
        ];

        myChart.update();
    }

    window.updateChart = updateChart;
}

function sendEmailWithChart() {
    const canvas = document.getElementById("myChart");
    if (!canvas) {
        alert("Chart not found!");
        return;
    }
    
    const imageData = canvas.toDataURL("image/png");

    fetch("/send-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chart: imageData })
    })
    .then(res => res.json())
    .then(() => alert("Email sent successfully"))
    .catch(err => {
        console.error("Email error:", err);
        alert("Failed to send email");
    });
}

window.sendEmailWithChart = sendEmailWithChart;

// DOM Ready handler
document.addEventListener("DOMContentLoaded", () => {
    // Task dropdown handlers
    document.querySelectorAll(".dropdown-item[data-value]").forEach(item => {
        item.addEventListener("click", function(e) {
            e.preventDefault();
            const value = Number(this.dataset.value);
            const img = this.dataset.img;
            
            const selectedImg = document.getElementById('selectedImg');
            const selectedValue = document.getElementById('selectedValue');
            
            if (selectedImg && selectedValue) {
                selectedImg.src = img;
                selectedValue.value = value;
            }
        });
    });

    // Task checkbox handlers
    document.querySelectorAll(".task-checkbox").forEach(cb => {
        cb.addEventListener("change", () => {
            fetch("/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: cb.dataset.id,
                    completed: cb.checked
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success && typeof updateChart === 'function') {
                    updateChart();
                }
            })
            .catch(err => console.error("Update error:", err));
        });
    });
    
    // Initial chart update
    if (typeof updateChart === 'function') {
        updateChart();
    }
});