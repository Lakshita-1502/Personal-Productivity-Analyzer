const ctx = document.getElementById("myChart");

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
        if (checkbox.checked) {
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

function sendEmailWithChart() {
    const canvas = document.getElementById("myChart");
    const imageData = canvas.toDataURL("image/png");

    fetch("/send-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chart: imageData })
    })
    .then(res => res.json())
    .then(() => alert("Email sent successfully"));
}

window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".dropdown-item").forEach(item=>{
        item.addEventListener("click", function(e){
            e.preventDefault();
            const value=Number(this.dataset.value);
            const img=this.dataset.img;
            document.getElementById('selectedImg').src = img;
            document.getElementById('selectedValue').value = value;
        });
    });

    document.querySelectorAll(".task-checkbox").forEach(cb => {
        cb.addEventListener("change", () => {
            fetch("/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id: cb.dataset.id,
                    completed: cb.checked
                })
            }).then(() => updateChart());
        });
    });
    updateChart();
});
