from __future__import unicode_literals
import frappe
from frappe import _

def calculate_lwp(self, holidays, working_days):
		lwp = 0
		holidays = "','".join(holidays)
		for d in range(working_days):
			dt = add_days(cstr(getdate(self.frm)), d)
			leave = frappe.db.sql("""
				SELECT t1.name,
					CASE WHEN t1.half_day_date = %(dt)s or t1.to_date = t1.from_date
					THEN t1.half_day else 0 END
				FROM `tabLeave Application` t1, `tabLeave Type` t2
				WHERE t2.name = t1.leave_type
				AND t2.is_lwp = 1
				AND t1.docstatus = 1
				AND t1.employee = %(employee)s
				AND CASE WHEN t2.include_holiday != 1 THEN %(dt)s not in ('{0}') and %(dt)s between from_date and to_date and ifnull(t1.salary_slip, '') = ''
				WHEN t2.include_holiday THEN %(dt)s between from_date and to_date and ifnull(t1.salary_slip, '') = ''
				END
				""".format(holidays), {"employee": self.employee, "dt": dt})

			if leave:
				lwp = cint(leave[0][1]) and (lwp + 0.5) or (lwp + 1)
		return lwp