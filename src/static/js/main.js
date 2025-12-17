const ctx = document.getElementById("myChart");

const myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["Completed", "Remaining"],
        datasets: [{
            data: [0, 100],
            backgroundColor: [
                'rgb(54, 162, 235)',
                'rgb(230, 230, 230)'
            ]
        }]
    }
});

function updateChart() {
    const productivity = Number(
        document.getElementById("productivity").textContent
    );

    myChart.data.datasets[0].data = [
        productivity,
        100 - productivity
    ];
    myChart.update();
}

function updateTotals() {
    let total = 0;
    let completed = 0;

    document.querySelectorAll("#tasklist li").forEach(li => {
        const points = Number(li.dataset.points);
        total += points;

        const checkbox = li.querySelector(".task-checkbox");
        if (checkbox.checked) {
            completed += points;
        }
    });

    document.getElementById("total").textContent = total;
    document.getElementById("completed-total").textContent = completed;
    document.getElementById("productivity").textContent =
        total === 0 ? "0" : ((completed / total) * 100).toFixed(1);
    updateChart();
}

window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".task-checkbox").forEach(cb => {
        cb.addEventListener("change", () => {
            fetch("/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: cb.dataset.id,
                    completed: cb.checked
                })
            }).then(() => updateTotals());
        });
    });
    updateTotals();
});
