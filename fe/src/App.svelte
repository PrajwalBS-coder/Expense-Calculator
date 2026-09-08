<script>
  import { onMount } from "svelte";
  import { createCategory, createExpense, generateReport, getDashboardData, login, register } from "./api";

  let token = localStorage.getItem("ledgerly_access");
  let authMode = "login";
  let form = { email: "", password: "", first_name: "", last_name: "" };
  let error = "";
  let busy = false;
  let data = null;
  let activeForm = "";
  let formError = "";
  let categoryForm = { name: "", description: "" };
  let expenseForm = { title: "", amount: "", expense_date: new Date().toISOString().slice(0, 10), category: "", description: "" };
  let reportMonth = new Date().toISOString().slice(0, 7);
  let report = null;
  let reportBusy = false;

  const money = (value) => new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" }).format(value || 0);
  const chartColors = ["#de765d", "#496b5b", "#d5aa47", "#7488a8", "#9b6a91", "#7a9b78"];
  const chartEntries = (breakdown) => {
    const entries = breakdown.filter((item) => Number(item.total) > 0);
    const visibleEntries = entries.slice(0, 5);
    const otherTotal = entries.slice(5).reduce((sum, item) => sum + Number(item.total), 0);
    return otherTotal ? [...visibleEntries, { category: "Other", total: otherTotal }] : visibleEntries;
  };
  const pieSlices = (breakdown) => {
    const entries = chartEntries(breakdown);
    const total = entries.reduce((sum, item) => sum + Number(item.total), 0);
    let start = 0;
    return entries.map((item, index) => {
      const end = start + (Number(item.total) / total) * 100;
      const slice = { ...item, color: chartColors[index], percentage: (Number(item.total) / total) * 100, start, end };
      start = end;
      return slice;
    });
  };
  const pieGradient = (breakdown) => {
    const slices = pieSlices(breakdown);
    return `conic-gradient(${slices.map((slice) => `${slice.color} ${slice.start}% ${slice.end}%`).join(", ")})`;
  };

  onMount(() => {
    if (token) loadDashboard();
  });

  async function loadDashboard() {
    try {
      const [categories, expenses, summary, breakdown, recurring] = await getDashboardData(token);
      data = { categories, expenses, summary, breakdown, recurring };
    } catch (requestError) {
      error = requestError.message;
    }
  }

  async function submitCategory() {
    formError = "";
    try {
      await createCategory(token, { ...categoryForm, type: "expense" });
      categoryForm = { name: "", description: "" };
      activeForm = "";
      await loadDashboard();
    } catch (requestError) {
      formError = requestError.message;
    }
  }

  async function submitExpense() {
    formError = "";
    try {
      await createExpense(token, { ...expenseForm, category: expenseForm.category || null });
      expenseForm = { title: "", amount: "", expense_date: new Date().toISOString().slice(0, 10), category: "", description: "" };
      activeForm = "";
      await loadDashboard();
    } catch (requestError) {
      formError = requestError.message;
    }
  }

  async function submitReport() {
    reportBusy = true;
    formError = "";
    try {
      const [summary, breakdown, budget] = await generateReport(token, reportMonth);
      report = { summary, breakdown, budget };
    } catch (requestError) {
      formError = requestError.message;
    } finally {
      reportBusy = false;
    }
  }

  async function submitAuth() {
    busy = true;
    error = "";
    try {
      if (authMode === "register") await register(form);
      const tokens = await login(form.email, form.password);
      token = tokens.access;
      localStorage.setItem("ledgerly_access", token);
      localStorage.setItem("ledgerly_refresh", tokens.refresh);
      await loadDashboard();
    } catch (requestError) {
      error = requestError.message;
    } finally {
      busy = false;
    }
  }

  function logout() {
    localStorage.removeItem("ledgerly_access");
    localStorage.removeItem("ledgerly_refresh");
    token = null;
    data = null;
  }
</script>

{#if !token}
  <main class="auth-page">
    <div class="auth-copy"><p class="eyebrow">PERSONAL FINANCE, MADE LEGIBLE</p><h1>Give every expense a place to land.</h1><p>One quiet workspace for tracking spending and the patterns hiding inside your month.</p></div>
    <form class="auth-card" on:submit|preventDefault={submitAuth}>
      <div class="brand-mark">L<span>/</span></div><h2>{authMode === "login" ? "Welcome back" : "Create your ledger"}</h2><p class="muted">{authMode === "login" ? "Pick up where you left off." : "Start with the essentials."}</p>
      {#if authMode === "register"}<div class="form-row"><input placeholder="First name" bind:value={form.first_name} required /><input placeholder="Last name" bind:value={form.last_name} required /></div>{/if}
      <input type="email" placeholder="Email address" bind:value={form.email} required /><input type="password" placeholder="Password" bind:value={form.password} required />
      {#if error}<p class="error">{error}</p>{/if}<button class="primary-button" disabled={busy}>{busy ? "Working..." : authMode === "login" ? "Open dashboard" : "Create account"}</button>
      <button type="button" class="text-button" on:click={() => (authMode = authMode === "login" ? "register" : "login")}>{authMode === "login" ? "Need an account? Register" : "Already registered? Log in"}</button>
    </form>
  </main>
{:else if error && !data}
  <main class="center-state"><p class="error">{error}</p><button class="primary-button" on:click={logout}>Sign out</button></main>
{:else if !data}
  <main class="center-state"><div class="loader"></div>Loading your ledger...</main>
{:else}
  <div class="app-shell">
    <aside><div class="brand-mark">L<span>/</span></div><nav><a class="active" href="/">Overview</a><a href="/">Expenses</a><a href="/">Recurring</a></nav><button class="logout" on:click={logout}>Sign out</button></aside>
    <main class="dashboard"><header><div><p class="eyebrow">SUNDAY, SEPTEMBER 6, 2026</p><h1>Your money, in focus.</h1></div><div class="header-actions"><button class="action-button" on:click={() => { activeForm = activeForm === "expense" ? "" : "expense"; formError = ""; }}>+ Expense</button><button class="action-button secondary" on:click={() => { activeForm = activeForm === "category" ? "" : "category"; formError = ""; }}>+ Category</button><button class="action-button report-button" on:click={() => { activeForm = activeForm === "report" ? "" : "report"; formError = ""; }}>Generate report</button><button class="avatar">ME</button></div></header>
      {#if activeForm === "report"}<section class="create-panel report-panel"><div class="panel-heading"><div><p class="eyebrow">REPORTING</p><h2>Generate a monthly report</h2></div><button class="close-button" on:click={() => (activeForm = "")}>Close</button></div><form class="report-form" on:submit|preventDefault={submitReport}><label for="report-month">Month</label><input id="report-month" type="month" bind:value={reportMonth} required /><button class="primary-button" disabled={reportBusy}>{reportBusy ? "Generating..." : "Generate report"}</button></form>{#if formError}<p class="error">{formError}</p>{/if}{#if report}<div class="report-results"><div><span>Total expenses</span><strong>{money(report.summary.total_expenses)}</strong></div></div>{#if report.breakdown.length}<h3>Category breakdown</h3>{#each report.breakdown as item}<div class="report-line"><span>{item.category_name || "Uncategorized"}</span><b>{money(item.total_expense)}</b></div>{/each}{/if}{#if report.budget.length}<h3>Budget status</h3>{#each report.budget as item}<div class="report-line"><span>{item.category_name}</span><b>{money(item.remaining)} remaining</b></div>{/each}{/if}{/if}</section>{/if}
      {#if activeForm}<section class="create-panel"><div class="panel-heading"><div><p class="eyebrow">QUICK ENTRY</p><h2>{activeForm === "expense" ? "Add an expense" : "Add a category"}</h2></div><button class="close-button" on:click={() => (activeForm = "")}>Close</button></div>{#if activeForm === "expense"}<form class="entry-form" on:submit|preventDefault={submitExpense}><input placeholder="What did you spend on?" bind:value={expenseForm.title} required /><input type="number" step="0.01" min="0.01" placeholder="Amount" bind:value={expenseForm.amount} required /><input type="date" bind:value={expenseForm.expense_date} required /><select bind:value={expenseForm.category}><option value="">No category</option>{#each data.categories as category}<option value={category.id}>{category.name}</option>{/each}</select><input placeholder="Note (optional)" bind:value={expenseForm.description} /><button class="primary-button">Save expense</button></form>{:else}<form class="entry-form" on:submit|preventDefault={submitCategory}><input placeholder="Category name" bind:value={categoryForm.name} required /><input placeholder="Description (optional)" bind:value={categoryForm.description} /><button class="primary-button">Save category</button></form>{/if}{#if formError}<p class="error">{formError}</p>{/if}</section>{/if}
      <section class="hero-grid"><div class="balance-panel"><p class="label">TOTAL EXPENSES THIS MONTH</p><strong>{money(data.summary.total_expenses)}</strong><div class="balance-foot"><span>Tracked spending</span><span>{data.expenses.length} entries</span></div></div><div class="stat-panel"><p class="label">ACTIVE ROUTINES</p><strong>{data.recurring.filter((item) => item.is_active).length}</strong><p class="muted">recurring expenses</p></div></section>
      <section class="content-grid"><div class="panel"><div class="panel-heading"><div><p class="eyebrow">LATEST ACTIVITY</p><h2>Recent expenses</h2></div><span class="count">{data.expenses.length} total</span></div>{#if data.expenses.length}<div class="expense-list">{#each data.expenses.slice(0, 5) as expense}<div class="expense-row"><div class="expense-icon">{expense.title.slice(0, 1).toUpperCase()}</div><div><strong>{expense.title}</strong><span>{expense.category_name || "Uncategorized"} · {expense.expense_date}</span></div><b>{money(expense.amount)}</b></div>{/each}</div>{:else}<p class="empty">Your first expense will appear here.</p>{/if}</div>
        <div class="panel breakdown"><div class="panel-heading"><div><p class="eyebrow">WHERE IT GOES</p><h2>Expense chart</h2></div></div>{#if data.breakdown.length}<div class="expense-chart"><div class="donut-chart" style={`background: ${pieGradient(data.breakdown)}`} role="img" aria-label="Expenses by category"><div><strong>{money(data.summary.total_expenses)}</strong><span>This month</span></div></div><div class="chart-legend">{#each pieSlices(data.breakdown) as item}<div class="legend-row"><span class="legend-color" style={`background: ${item.color}`}></span><span>{item.category}</span><b>{item.percentage.toFixed(0)}% · {money(item.total)}</b></div>{/each}</div></div>{:else}<p class="empty">Add expenses to see patterns.</p>{/if}</div></section>
    </main>
  </div>
{/if}
