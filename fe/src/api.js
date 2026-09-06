const API_ROOT = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

let refreshRequest;

async function refreshAccessToken() {
  const refresh = localStorage.getItem("ledgerly_refresh");
  if (!refresh) return null;

  refreshRequest ||= fetch(`${API_ROOT}/users/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  })
    .then(async (response) => {
      if (!response.ok) throw new Error("Session expired");
      const tokens = await response.json();
      localStorage.setItem("ledgerly_access", tokens.access);
      return tokens.access;
    })
    .catch(() => {
      localStorage.removeItem("ledgerly_access");
      localStorage.removeItem("ledgerly_refresh");
      return null;
    })
    .finally(() => {
      refreshRequest = null;
    });

  return refreshRequest;
}

async function request(path, options = {}) {
  let response = await fetch(`${API_ROOT}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  if (response.status === 401 && !options.skipRefresh) {
    const access = await refreshAccessToken();
    if (access) {
      response = await fetch(`${API_ROOT}${path}`, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...(options.headers || {}),
          Authorization: `Bearer ${access}`,
        },
      });
    }
  }

  const body = response.status === 204 ? null : await response.json();
  if (!response.ok) {
    throw new Error(
      body?.detail || Object.values(body || {})[0]?.[0] || "Request failed",
    );
  }
  return body;
}

export function login(email, password) {
  return request("/users/login/", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function register(payload) {
  return request("/users/create/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function createCategory(token, payload) {
  return request("/expenses/categories/", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export function createExpense(token, payload) {
  return request("/expenses/expenses/", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export function getDashboardData(token) {
  const headers = { Authorization: `Bearer ${token}` };
  const month = new Date().toISOString().slice(0, 7);
  return Promise.all([
    request("/expenses/categories/?type=expense", { headers }),
    request("/expenses/expenses/?sort=date_desc", { headers }),
    request(`/expenses/reports/monthly-summary/?month=${month}`, { headers }),
    request(`/expenses/reports/category-breakdown/?month=${month}`, {
      headers,
    }),
    request("/expenses/recurring-expenses/", { headers }),
  ]).then(([categories, expenses, summary, breakdown, recurring]) => [
    categories,
    expenses,
    summary,
    breakdown.map((item) => ({
      category: item.category_name || "Uncategorized",
      total: item.total_expense,
    })),
    recurring,
  ]);
}

export function generateReport(token, month) {
  const headers = { Authorization: `Bearer ${token}` };
  return Promise.all([
    request(`/expenses/reports/monthly-summary/?month=${month}`, { headers }),
    request(`/expenses/reports/category-breakdown/?month=${month}`, {
      headers,
    }),
    request(`/expenses/reports/budget-vs-spent/?month=${month}`, { headers }),
  ]);
}
