const form = document.getElementById('predict-form');
const submitBtn = document.getElementById('submit-btn');
const results = document.getElementById('results');
const resultsBody = document.getElementById('results-body');
const errorBox = document.getElementById('form-error');

const MODEL_LABELS = {
  LR_v1: 'Linear Regression',
  Polynomial_v1: 'Polynomial Regression',
};

const FIELDS = [
  { id: 'age',         min: 14,  max: 90,  integer: true  },
  { id: 'body_weight', min: 40,  max: 200, integer: false },
  { id: 'squat',       min: 0,   max: 600, integer: false },
  { id: 'deadlift',    min: 0,   max: 700, integer: false },
];

function setFieldError(input, message) {
  input.classList.add('input-error');
  const hint = document.createElement('span');
  hint.className = 'field-hint';
  hint.textContent = message;
  input.parentNode.appendChild(hint);
}

function clearFieldError(input) {
  input.classList.remove('input-error');
  const hint = input.parentNode.querySelector('.field-hint');
  if (hint) hint.remove();
}

function clearAllErrors() {
  FIELDS.forEach(f => clearFieldError(document.getElementById(f.id)));
  errorBox.classList.remove('visible');
}

function validate() {
  clearAllErrors();
  let valid = true;

  for (const f of FIELDS) {
    const input = document.getElementById(f.id);
    const raw = input.value.trim();

    if (!raw) {
      setFieldError(input, 'Заполните поле');
      valid = false;
      continue;
    }

    if (f.integer && raw.includes('.')) {
      setFieldError(input, 'Только целое число');
      valid = false;
      continue;
    }

    const num = f.integer ? parseInt(raw, 10) : parseFloat(raw);

    if (isNaN(num)) {
      setFieldError(input, 'Введите корректное число');
      valid = false;
      continue;
    }

    if (num < f.min || num > f.max) {
      setFieldError(input, `От ${f.min} до ${f.max}`);
      valid = false;
    }
  }

  return valid;
}

FIELDS.forEach(f => {
  document.getElementById(f.id).addEventListener('input', function () {
    clearFieldError(this);
  });
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  if (!validate()) return;

  errorBox.classList.remove('visible');
  results.classList.remove('visible');
  submitBtn.textContent = 'Вычисляю...';
  submitBtn.classList.add('loading');

  const payload = {
    age: parseInt(document.getElementById('age').value, 10),
    body_weight: parseFloat(document.getElementById('body_weight').value),
    squat: parseFloat(document.getElementById('squat').value),
    deadlift: parseFloat(document.getElementById('deadlift').value),
  };

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      const detail = data.detail;
      const message = Array.isArray(detail)
        ? detail.map(e => e.msg || 'Ошибка валидации').join('; ')
        : (detail || `Ошибка сервера (${res.status})`);
      throw new Error(message);
    }

    const data = await res.json();
    renderResults(data.predictions);
  } catch (err) {
    errorBox.textContent = err.message || 'Не удалось получить предсказание. Попробуй ещё раз.';
    errorBox.classList.add('visible');
  } finally {
    submitBtn.textContent = 'Предсказать';
    submitBtn.classList.remove('loading');
  }
});

function renderResults(predictions) {
  resultsBody.innerHTML = '';

  for (const [key, value] of Object.entries(predictions)) {
    const label = MODEL_LABELS[key] ?? key;
    const row = document.createElement('div');
    row.className = 'prediction-row';
    row.innerHTML = `
      <span class="prediction-name">${label}</span>
      <span class="prediction-value">${value}<span class="kg">kg</span></span>
    `;
    resultsBody.appendChild(row);
  }

  results.classList.add('visible');
  results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
