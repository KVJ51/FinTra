docudocument.addEventListener("DOMContentLoaded", () => {
    const askBtn = document.querySelector("#ask-btn");
    const questionInput = document.querySelector ("#question");
    const responseBox = document.querySelector("#response");
   


    askBtn.addEventListener("click", async () => {
      const question = questionInput.value.trim();
      if (!question) return;
 
      responseBox.innerHTML = "Thinking...";
 
      try {
        const res = await fetch("/ask-financial", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ question }),
        });
 
        const data = await res.json();
        if (data.answer) {
          responseBox.innerHTML = data.answer;
        } else {
          responseBox.innerHTML = data.error || "Something went wrong!";
        }
      } catch (err) {
        console.error(err);
        responseBox.innerHTML = "Error contacting server.";
      }
    });
  });
   
  document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector("#some-button");
    if (btn) {
        btn.addEventListener("click", () => {
            console.log("Button clicked");
        });
    }
    const sales = parseFloat(document.getElementById("data-sales").value) || 0;
    const production_cost = parseFloat(document.getElementById("data-production").value) || 0;
    const salary = parseFloat(document.getElementById("data-salary").value) || 0;
    const overheads = parseFloat(document.getElementById("data-overheads").value) || 0;
    const net_profit = parseFloat(document.getElementById("data-net-profit").value) || 0;


    const expenses = production_cost + salary + overheads;


    const ctx = document.getElementById("spendingChart").getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Sales", "Expenses", "Net Profit"],
            datasets: [{
                label: "Amount (₹)",
                data: [sales, expenses, net_profit],
                backgroundColor: [
                    "rgba(54, 162, 235, 0.7)",
                    "rgba(255, 99, 132, 0.7)",
                    "rgba(75, 192, 192, 0.7)"
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });


    // Forecast chart logic...
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const predicted_income = [sales, sales * 1.1, sales * 1.15, sales * 1.2, sales * 1.25, sales * 1.3];
    const predicted_expenses = [expenses, expenses * 1.05, expenses * 1.1, expenses * 1.15, expenses * 1.2, expenses * 1.25];
    const predicted_profit = predicted_income.map((income, i) => income - predicted_expenses[i]);


    const predictionCtx = document.getElementById("predictionChart").getContext("2d");
    new Chart(predictionCtx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: 'Predicted Income',
                    data: predicted_income,
                    borderColor: 'green',
                    backgroundColor: 'rgba(0, 128, 0, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Predicted Expenses',
                    data: predicted_expenses,
                    borderColor: 'red',
                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Predicted Profit',
                    data: predicted_profit,
                    borderColor: 'blue',
                    backgroundColor: 'rgba(0, 0, 255, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Financial Trend Forecast',
                    font: { size: 18 }
                }
            }
        }
    });
});


 
ment.addEventListener("DOMContentLoaded", () => {
    const askBtn = document.querySelector("#ask-btn");
    const questionInput = document.querySelector ("#question");
    const responseBox = document.querySelector("#response");
   


    askBtn.addEventListener("click", async () => {
      const question = questionInput.value.trim();
      if (!question) return;
 
      responseBox.innerHTML = "Thinking...";
 
      try {
        const res = await fetch("/ask-financial", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ question }),
        });
 
        const data = await res.json();
        if (data.answer) {
          responseBox.innerHTML = data.answer;
        } else {
          responseBox.innerHTML = data.error || "Something went wrong!";
        }
      } catch (err) {
        console.error(err);
        responseBox.innerHTML = "Error contacting server.";
      }
    });
  });
   
  document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector("#some-button");
    if (btn) {
        btn.addEventListener("click", () => {
            console.log("Button clicked");
        });
    }
    const sales = parseFloat(document.getElementById("data-sales").value) || 0;
    const production_cost = parseFloat(document.getElementById("data-production").value) || 0;
    const salary = parseFloat(document.getElementById("data-salary").value) || 0;
    const overheads = parseFloat(document.getElementById("data-overheads").value) || 0;
    const net_profit = parseFloat(document.getElementById("data-net-profit").value) || 0;


    const expenses = production_cost + salary + overheads;


    const ctx = document.getElementById("spendingChart").getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Sales", "Expenses", "Net Profit"],
            datasets: [{
                label: "Amount (₹)",
                data: [sales, expenses, net_profit],
                backgroundColor: [
                    "rgba(54, 162, 235, 0.7)",
                    "rgba(255, 99, 132, 0.7)",
                    "rgba(75, 192, 192, 0.7)"
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });


    // Forecast chart logic...
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const predicted_income = [sales, sales * 1.1, sales * 1.15, sales * 1.2, sales * 1.25, sales * 1.3];
    const predicted_expenses = [expenses, expenses * 1.05, expenses * 1.1, expenses * 1.15, expenses * 1.2, expenses * 1.25];
    const predicted_profit = predicted_income.map((income, i) => income - predicted_expenses[i]);


    const predictionCtx = document.getElementById("predictionChart").getContext("2d");
    new Chart(predictionCtx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: 'Predicted Income',
                    data: predicted_income,
                    borderColor: 'green',
                    backgroundColor: 'rgba(0, 128, 0, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Predicted Expenses',
                    data: predicted_expenses,
                    borderColor: 'red',
                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Predicted Profit',
                    data: predicted_profit,
                    borderColor: 'blue',
                    backgroundColor: 'rgba(0, 0, 255, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Financial Trend Forecast',
                    font: { size: 18 }
                }
            }
        }
    });
});


 

