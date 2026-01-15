import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import re

# Заголовок приложения
st.title("Кредитный калькулятор")

# Форма ввода данных
st.subheader("Введите параметры кредита")

with st.form("credit_form"):
    amount = st.text_input("Сумма кредита (руб.)", value="")
    rate = st.text_input("Годовая процентная ставка (%)", value="")
    term = st.text_input("Срок кредита (месяцев)", value="")
    payment_type = st.radio("Тип платежа", ["Аннуитетный", "Дифференциальный"])
    start_date = st.date_input("Дата первого платежа", value=None)

    submitted = st.form_submit_button("Рассчитать")

# Проверка и обработка ввода
if submitted:
    # Валидация ввода
    errors = []

    if not amount or not re.match(r"^\d+(\.\d+)?$", amount) or float(amount) <= 0:
        errors.append("Сумма кредита должна быть положительным числом.")
    
    if not rate or not re.match(r"^\d+(\.\d+)?$", rate) or float(rate) < 0:
        errors.append("Процентная ставка должна быть неотрицательным числом.")
    
    if not term or not term.isdigit() or int(term) <= 0:
        errors.append("Срок кредита должен быть целым положительным числом (месяцев).")
    
    if start_date is None:
        errors.append("Укажите дату первого платежа.")

    if errors:
        st.error("Исправьте ошибки:")
        for error in errors:
            st.write(f"- {error}")
        st.stop()

    # Преобразование в числа
    amount = float(amount)
    rate = float(rate) / 100  # в долях
    term = int(term)

    # Расчёт месячной процентной ставки
    monthly_rate = rate / 12

    # Аннуитетный платёж
    if payment_type == "Аннуитетный":
        if monthly_rate == 0:
            monthly_payment = amount / term
        else:
            monthly_payment = amount * monthly_rate * (1 + monthly_rate) ** term / \
                            ((1 + monthly_rate) ** term - 1)
        
        # Формирование графика
        data = []
        balance = amount
        for month in range(1, term + 1):
            interest = balance * monthly_rate
            principal = monthly_payment - interest
            balance -= principal
            if balance < 0:
                balance = 0
            payment_date = start_date + timedelta(days=30 * (month - 1))
            data.append({
                "Месяц": month,
                "Дата платежа": payment_date.strftime("%d.%m.%Y"),
                "Остаток долга на начало": round(balance + principal, 2),
                "Ежемесячный платёж": round(monthly_payment, 2),
                "Процентная часть": round(interest, 2),
                "Долговая часть": round(principal, 2),
                "Остаток долга на конец": round(balance, 2)
            })
        df = pd.DataFrame(data)

    # Дифференцированный платёж
    else:
        principal_part = amount / term
        data = []
        balance = amount
        for month in range(1, term + 1):
            interest = balance * monthly_rate
            payment = principal_part + interest
            balance -= principal_part
            if balance < 0:
                balance = 0
            payment_date = start_date + timedelta(days=30 * (month - 1))
            data.append({
                "Месяц": month,
                "Дата платежа": payment_date.strftime("%d.%m.%Y"),
                "Остаток долга на начало": round(balance + principal_part, 2),
                "Ежемесячный платёж": round(payment, 2),
                "Процентная часть": round(interest, 2),
                "Долговая часть": round(principal_part, 2),
                "Остаток долга на конец": round(balance, 2)
            })
        df = pd.DataFrame(data)

    # Вывод результата
    st.subheader("График платежей")
    st.dataframe(df)

    # Дополнительная информация
    total_payment = df["Ежемесячный платёж"].sum()
    total_interest = total_payment - amount
    st.write(f"**Общая сумма выплат:** {round(total_payment, 2)} руб.")
    st.write(f"**Переплата по кредиту:** {round(total_interest, 2)} руб.")

    # Условный рендеринг
    with st.expander("Подробнее о расчётах"):
        st.write(f"Сумма кредита: {amount} руб.")
        st.write(f"Годовая ставка: {rate * 100:.2f} %")
        st.write(f"Срок: {term} месяцев")
        st.write(f"Тип платежа: {payment_type}")
        st.write(f"Дата первого платежа: {start_date.strftime('%d.%m.%Y')}")


else:
    st.info("Заполните форму и нажмите «Рассчитать», чтобы увидеть график платежей.")