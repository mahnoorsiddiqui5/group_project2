import streamlit as st
import pandas as pd
import data_simulator
import diagnostic_brain
st.set_page_config(
   page_title="ASTRONAUT VITAL SINGS AND HEALTH MONITOR", 
   page_icon="🚀",
   layout="wide",
   initial_sidebar_state="collapsed"
)
data_simulator.simulate()
df= pd.read_csv("astronaut_vitals.csv")
latest=df.iloc[-1]
st.title("BIO-TELEMETRY AND CREW WELLNESS MONITOR🧑‍⚕️")
st.caption("REAL-TIME TELEMETRY")
st.divider()
col1,col2,col3=st.columns(3)
heart_rate=int(latest["heart_rate"])
if 60<=heart_rate<=100:
   heart_rate_delta="NORMAL"
   heart_rate_color="normal"
else:
   heart_rate_delta=f"Alert:Out of range"
   heart_rate_color="inverse"
with col1:
   with st.container(border=True):
    st.metric(label="Heart rate🫀",
              value=f"{heart_rate}BPM",
              delta=heart_rate_delta,
              delta_color=heart_rate_color)
    if 60<=heart_rate<=100:
          st.success("HEART RATE IS NORMAL")
    else:
          st.error("WARNING:HEART RATE IS NOT NORMAL")
blood_oxygen=int(latest["blood_oxygen"])
if 95<=blood_oxygen<=100:
   blood_oxygen_delta="NORMAL"
   blood_oxygen_color="normal"
else:
   blood_oxygen_delta="Low Oxygen"
   blood_oxygen_color="inverse"
with col2:
   with st.container(border=True):
    st.metric(label="Blood Oxygen🩸",
              value=f"{blood_oxygen}%",
              delta=blood_oxygen_delta,
              delta_color=blood_oxygen_color)
    if 95<=blood_oxygen<=100:
       st.success("BLOOD OXYGEN IS NORMAL")
    else:
       st.error("WARNING:BLOOD OXYGEN IS NOT NORMAL")
c_temp=int(latest['core_bodyTemp'])
if 36.5<=c_temp<=37.5:
   c_temp_delta="NORMAL"
   c_temp_color="normal"
elif c_temp<36.5:
   c_temp_color="inverse"
   c_temp_delta="LOW (HYPOTHERMIA)"
else:
   c_temp_delta="HIGH (FEVER)"
   c_temp_color="inverse"
with col3:
   with st.container(border=True):
    st.metric(
       label="CORE TEMPERATURE🌡️",
       value=f"{c_temp}ºC",
       delta=c_temp_delta,
       delta_color=c_temp_color)
    if 36.5<=c_temp<=37.5:
       st.success("CORE TEMPERATURE IS NORMAL")
    else:
       st.error("WARNING:CORE TEMPERATURE IS NOT NORMAL")
sbp=int(latest["systolic_bloodPressure"])
if 90<=sbp<=120:
   sbp_delta="NORMAL"
   sbp_delta_color="normal"
else:
   sbp_delta="LOW"
   sbp_delta_color="inverse"
col4,col5,col6=st.columns(3)
with col4:
   with st.container(border=True):
    st.metric(label="Sytolic Blood Pressure🩸",
              value=f"{sbp}mmHg",
              delta=sbp_delta,
              delta_color=sbp_delta_color)
    if 90<=sbp<=120:
       st.success("SYSTOLIC BLOOD PRESSURE IS NORMAL")
    else: 
       st.error("SYSTOLIIC BLOOD PRESSURE IS NOT NORMAL")
slp_hrs=int(latest["sleep_hours"])
if 6<=slp_hrs<=7:
   slp_hrs_delta="NORMAL"
   slp_hrs_color="normal"
else:
   slp_hrs_delta="REST DEFECIT"
   slp_hrs_color="inverse"
with col5:
   with st.container(border=True):
    st.metric(label="Sleep Hours😴",
              value=f"{slp_hrs} hours",
              delta=slp_hrs_delta,
              delta_color=slp_hrs_color)
    if 6<=slp_hrs<=7:
       st.success("SLEEP HOURS ARE NORMAL")
    else: 
       st.error("SLEEP HOURS ARE NOT NORMAL")     
rad=int(latest["radiation_exposure"])
if 0<=rad<=0.5:
   rad_delta="NORMAL"
   rad_color="normal"
else:
   rad_delta="HIGH RADIATION"
   rad_color="inverse"
with col6:
   with st.container(border=True):
    st.metric(label="Radiatiion Exposure☢️",
              value=f"{rad} mSv/h",
              delta=rad_delta,
              delta_color=rad_color)
    if 0<=rad<=0.5:
       st.success("RADIATION EXPOSURE IS NORMAL")
    else: 
       st.error("RADIATION EXPOSURE IS HIGH")  
st.divider()
chart_col, log_col = st.columns([2, 2])

with chart_col:
  st.subheader("📈 All Telemetry Trends (14 Days)")

  
  chart_df = df.set_index("day")

  
  trends_df = chart_df[[
      "heart_rate",
      "blood_oxygen",
      "core_bodyTemp",
      "systolic_bloodPressure",
      "sleep_hours",
      "radiation_exposure",
  ]]

  st.line_chart(trends_df, height=350)
  st.caption(
      "Tracking all 6 vital signs and environmental parameters across the"
      " 14-day simulation."
  )

with log_col:
  st.subheader("📋 Recent Mission Logs")
  st.dataframe(
      df.tail(5).sort_values(by="day", ascending=True),
      use_container_width=True,
      hide_index=True,
  )
  st.caption("Showing the 5 most recent daily telemetry records.")
st.divider()
df=pd.read_csv("astronaut_vitals.csv")
latest=df.iloc[-1].to_dict()
recent=diagnostic_brain.get_recent_days(3)
evaluation=diagnostic_brain.evaluate_health(latest,recent)
status=evaluation["status"]
if status=="Nominal":
   st.success(f"Health Staus:{status} 🟢")
if status=="Caution":
   st.warning(f"Health Staus:{status} 🟡")
if status=="Action Required":
   st.error(f"Health Staus:{status} 🔴")
with st.expander("🩺Medical Briefing"):
   for alert in evaluation["alerts"]:
    st.markdown(f"- ⚠️ {alert}")

   for rec in evaluation["recommendations"]:
     st.markdown(f"- ✅ {rec}")
