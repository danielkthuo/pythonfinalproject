// Budget Form Handling
document.addEventListener('DOMContentLoaded', function() {
    // Budget form submission
    const budgetForm = document.getElementById('budgetForm');
    if (budgetForm) {
        budgetForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            fetch('/api/budget', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                alert('Budget created successfully!');
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error creating budget');
            });
        });
    }

    // Donation form handling
    const donationForms = document.querySelectorAll('.donation-form');
    donationForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                campaign_id: formData.get('campaign_id'),
                amount: parseFloat(formData.get('amount')),
                anonymous: formData.get('anonymous') === 'on',
                message: formData.get('message')
            };

            fetch('/api/donate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                alert('Donation successful! Thank you for your support.');
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error processing donation');
            });
        });
    });

    // Loan application form
    const loanForm = document.getElementById('loanForm');
    if (loanForm) {
        loanForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            fetch('/api/loan-application', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                alert('Loan application submitted successfully!');
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error submitting application');
            });
        });
    }

    // Calculate budget totals
    const incomeInput = document.getElementById('income');
    if (incomeInput) {
        incomeInput.addEventListener('input', calculateBudgetSummary);
    }

    const expenseInputs = document.querySelectorAll('input[class*="form-control"]');
    expenseInputs.forEach(input => {
        input.addEventListener('input', calculateBudgetSummary);
    });
});

function calculateBudgetSummary() {
    const income = parseFloat(document.getElementById('income')?.value) || 0;
    const housing = parseFloat(document.getElementById('housing')?.value) || 0;
    const food = parseFloat(document.getElementById('food')?.value) || 0;
    const transportation = parseFloat(document.getElementById('transportation')?.value) || 0;
    const healthcare = parseFloat(document.getElementById('healthcare')?.value) || 0;
    const education = parseFloat(document.getElementById('education')?.value) || 0;
    const savings = parseFloat(document.getElementById('savings')?.value) || 0;
    const other = parseFloat(document.getElementById('other')?.value) || 0;

    const totalExpenses = housing + food + transportation + healthcare + education + savings + other;
    const remaining = income - totalExpenses;

    const summaryElement = document.getElementById('budgetSummary');
    if (summaryElement) {
        summaryElement.innerHTML = `
            <h5>Budget Summary</h5>
            <p>Total Income: $${income.toFixed(2)}</p>
            <p>Total Expenses: $${totalExpenses.toFixed(2)}</p>
            <p class="${remaining < 0 ? 'text-danger' : 'text-success'}">
                Remaining: $${remaining.toFixed(2)}
            </p>
            ${remaining < 0 ? '<div class="alert alert-warning">Warning: You are over budget!</div>' : ''}
        `;
    }
}