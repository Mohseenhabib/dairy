# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class RMRDLines(Document):
	def calculate_total_cans_wt(self):
		g_cow_milk = self.g_cow_milk if self.g_cow_milk else 0
		g_buf_milk = self.g_buf_milk if self.g_buf_milk else 0
		g_mix_milk = self.g_mix_milk if self.g_mix_milk else 0
		g_total_m = g_cow_milk + g_buf_milk + g_mix_milk

		g_cow_milk_can = self.g_cow_milk_can if self.g_cow_milk_can else 0
		g_buf_milk_can = self.g_buf_milk_can if self.g_buf_milk_can else 0
		g_mix_milk_can = self.g_mix_milk_can if self.g_mix_milk_can else 0
		g_total_c = g_cow_milk_can + g_buf_milk_can + g_mix_milk_can

		s_cow_milk = self.s_cow_milk if self.s_cow_milk else 0
		s_buf_milk = self.s_buf_milk if self.s_buf_milk else 0
		s_mix_milk = self.s_mix_milk if self.s_mix_milk else 0
		s_total_m = s_cow_milk + s_buf_milk + s_mix_milk

		s_cow_milk_can = self.s_cow_milk_can if self.s_cow_milk_can else 0
		s_buf_milk_can = self.s_buf_milk_can if self.s_buf_milk_can else 0
		s_mix_milk_can = self.s_mix_milk_can if self.s_mix_milk_can else 0
		s_total_c = s_cow_milk_can + s_buf_milk_can + s_mix_milk_can

		c_cow_milk = self.c_cow_milk if self.c_cow_milk else 0
		c_buf_milk = self.c_buf_milk if self.c_buf_milk else 0
		c_mix_milk = self.c_mix_milk if self.c_mix_milk else 0
		c_total_m =c_cow_milk + c_buf_milk + c_mix_milk

		c_cow_milk_can = self.c_cow_milk_can if self.c_cow_milk_can else 0
		c_buf_milk_can = self.c_buf_milk_can if self.c_buf_milk_can else 0
		c_mix_milk_can = self.c_mix_milk_can if self.c_mix_milk_can else 0
		c_total_c = c_cow_milk_can + c_buf_milk_can + c_mix_milk_can

		self.total_milk_can = g_total_c - s_total_c - c_total_c
		self.total_milk_wt = g_total_m - s_total_m - c_total_m
		self.db_update()