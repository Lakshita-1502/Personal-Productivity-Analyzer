function updateTotal() {
    let total = 0;
    document.querySelectorAll("#tasklist li").forEach(cb => {
        total += Number(cb.dataset.points);
    });
    document.getElementById("total").textContent = total;
}

function updateCompletedTotal(){
    let completedTotal=0;
    document.querySelectorAll("#tasklist li input.task-checkbox:checked").forEach(cb => {
        completedTotal+=Number(cb.dataset.points);
    });
    document.getElementById("completed-total").textContent=completedTotal;
}

function calcProductivity(){
    let total=Number(document.getElementById("total").textContent);
    let completed=Number(document.getElementById("completed-total").textContent);
    if (total==0){
        document.getElementById("productivity").textContent="0.0";
        return;
    }
    let productivity=(completed/total)*100;
    document.getElementById("productivity").textContent=productivity.toFixed(1);
}

function recallAll(){
    updateTotal();
    updateCompletedTotal();
    calcProductivity();
}

function deleteTask(){
    const li=btn.closest("li");
    const points=Number(li.dataset.points);
    let total=Number(document.getElementById("total").textContent);

    total=total-points;
    document.getElementById("total").textContent=total;

    const checkbox=li.querySelector(".task-checkbox");
    if (checkbox.checked){}
}

window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".task-checkbox").forEach(cb => {
        cb.addEventListener("change", recallAll);
    });
    recallAll();
});
