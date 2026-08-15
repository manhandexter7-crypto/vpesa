const API = "/api";

function getToken() {
    return localStorage.getItem("vpesa_access");
}

function authHeaders() {

    return {
        "Content-Type": "application/json",
        "Authorization":
            "Bearer " + getToken()
    };
}


async function refreshBalance() {

    const response = await fetch(
        API + "/transactions/balance/",
        {
            headers: authHeaders()
        }
    );

    if (!response.ok) {
        return;
    }

    const data = await response.json();

    document.getElementById(
        "balance"
    ).textContent = Number(
        data.balance
    ).toFixed(2);
}


async function loadTransactions() {

    const response = await fetch(
        API + "/transactions/history/",
        {
            headers: authHeaders()
        }
    );

    if (!response.ok) {
        return;
    }

    const data = await response.json();

    const container =
        document.getElementById(
            "transaction-list"
        );

    container.innerHTML = "";

    data.forEach(tx => {

        const item =
            document.createElement("div");

        item.className = "transaction";

        item.innerHTML = `
            <strong>${tx.type}</strong>
            <br>
            KSh ${tx.amount}
            <br>
            <small>
                ${tx.status}
            </small>
            <br>
            <small>
                ${tx.reference}
            </small>
        `;

        container.appendChild(item);
    });
}


function showDeposit() {

    document.getElementById(
        "form-area"
    ).innerHTML = `

        <div class="form">

            <h2>Sandbox Deposit</h2>

            <input
                id="depositAmount"
                type="number"
                placeholder="Amount"
            >

            <button onclick="deposit()">
                Deposit Test Money
            </button>

        </div>
    `;
}


function showWithdraw() {

    document.getElementById(
        "form-area"
    ).innerHTML = `

        <div class="form">

            <h2>Sandbox Withdrawal</h2>

            <input
                id="withdrawAmount"
                type="number"
                placeholder="Amount"
            >

            <button onclick="withdraw()">
                Withdraw Test Money
            </button>

        </div>
    `;
}


function showSend() {

    document.getElementById(
        "form-area"
    ).innerHTML = `

        <div class="form">

            <h2>Send VPesa</h2>

            <input
                id="recipient"
                type="text"
                placeholder="Recipient phone"
            >

            <input
                id="sendAmount"
                type="number"
                placeholder="Amount"
            >

            <input
                id="description"
                type="text"
                placeholder="Description"
            >

            <button onclick="sendMoney()">
                Send
            </button>

        </div>
    `;
}


async function deposit() {

    const amount =
        document.getElementById(
            "depositAmount"
        ).value;

    const response = await fetch(
        API + "/transactions/deposit/",
        {
            method: "POST",

            headers: {
                ...authHeaders(),
                "Idempotency-Key":
                    crypto.randomUUID()
            },

            body: JSON.stringify({
                amount: amount
            })
        }
    );

    const data =
        await response.json();

    alert(
        data.reference ||
        data.error ||
        "Deposit completed"
    );

    await refreshBalance();
    await loadTransactions();
}


async function withdraw() {

    const amount =
        document.getElementById(
            "withdrawAmount"
        ).value;

    const response = await fetch(
        API + "/transactions/withdraw/",
        {
            method: "POST",

            headers: {
                ...authHeaders(),
                "Idempotency-Key":
                    crypto.randomUUID()
            },

            body: JSON.stringify({
                amount: amount
            })
        }
    );

    const data =
        await response.json();

    alert(
        data.reference ||
        data.error ||
        "Withdrawal completed"
    );

    await refreshBalance();
    await loadTransactions();
}


async function sendMoney() {

    const recipient =
        document.getElementById(
            "recipient"
        ).value;

    const amount =
        document.getElementById(
            "sendAmount"
        ).value;

    const description =
        document.getElementById(
            "description"
        ).value;

    const response = await fetch(
        API + "/transactions/transfer/",
        {
            method: "POST",

            headers: {
                ...authHeaders(),
                "Idempotency-Key":
                    crypto.randomUUID()
            },

            body: JSON.stringify({

                recipient_phone:
                    recipient,

                amount:
                    amount,

                description:
                    description
            })
        }
    );

    const data =
        await response.json();

    alert(
        data.reference ||
        data.error ||
        "Transfer completed"
    );

    await refreshBalance();
    await loadTransactions();
}


function logout() {

    localStorage.removeItem(
        "vpesa_access"
    );

    localStorage.removeItem(
        "vpesa_refresh"
    );

    window.location.href =
        "/login/";
}


refreshBalance();
loadTransactions();