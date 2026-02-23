import pandas as pd
import json
import os

class ReportService:

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def load_data(self):
        try:
            students_file = os.path.join(self.input_path, "students.csv")
            attendance_file = os.path.join(self.input_path, "attendance.csv")

            students = pd.read_csv(students_file)
            attendance = pd.read_csv(attendance_file)

            return students, attendance

        except FileNotFoundError as e:
            print("❌ Required file missing:", e)
            exit()

    def clean_data(self, students, attendance):
        # remove duplicates
        students = students.drop_duplicates()
        attendance = attendance.drop_duplicates()

        # handle missing values
        students["marks"] = pd.to_numeric(students["marks"], errors="coerce").fillna(0)
        attendance["attendancePercent"] = pd.to_numeric(
            attendance["attendancePercent"], errors="coerce"
        ).fillna(0)

        return students, attendance

    def generate_report(self, students, attendance):
        merged = pd.merge(students, attendance, on="studentId", how="left")

        # average marks per student
        merged["avgMarks"] = merged["marks"]

        # status
        merged["status"] = merged["avgMarks"].apply(
            lambda x: "PASS" if x >= 50 else "FAIL"
        )

        report = merged[
            ["studentId", "name", "attendancePercent", "avgMarks", "status"]
        ]

        return report

    def generate_summary(self, report):
        total_students = len(report)
        avg_attendance = report["attendancePercent"].mean()
        avg_marks = report["avgMarks"].mean()
        pass_count = (report["status"] == "PASS").sum()
        fail_count = (report["status"] == "FAIL").sum()

        top3 = (
            report.sort_values(by="avgMarks", ascending=False)
            .head(3)["name"]
            .tolist()
        )

        summary = {
            "totalStudents": int(total_students),
            "avgAttendance": round(avg_attendance, 2),
            "avgMarks": round(avg_marks, 2),
            "passCount": int(pass_count),
            "failCount": int(fail_count),
            "top3Students": top3,
        }

        return summary

    def save_outputs(self, report, summary):
        os.makedirs(self.output_path, exist_ok=True)

        report.to_csv(os.path.join(self.output_path, "report.csv"), index=False)

        with open(os.path.join(self.output_path, "summary.json"), "w") as f:
            json.dump(summary, f, indent=4)

    def run(self):
        students, attendance = self.load_data()
        students, attendance = self.clean_data(students, attendance)
        report = self.generate_report(students, attendance)
        summary = self.generate_summary(report)
        self.save_outputs(report, summary)

        print("✅ Reports generated successfully!")