// Backend location, shared by every page.
const API_BASE_URL = "";
// const API_BASE_URL = "http://127.0.0.1:8000";

// Wake the backend as early as possible. The free host sleeps when idle, so
// this request starts the wake-up while the page is still loading and the
// visitor is reading or filling in the form. The response is ignored.
fetch(`${API_BASE_URL}/health`, { mode: "no-cors", cache: "no-store" }).catch(() => {});
