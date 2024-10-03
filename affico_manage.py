def manageAfficoV2(excel):
		timeInterval = ForexClass.timeInterval

		data = {}
		response = {
			"result":0,
			"error":"",
			"data":{}
		}
		requ=request.get_json()
		if request.headers.get('Authorization'):
			user = ForexClass.getUserSession(request.headers.get('Authorization').replace("Bearer ", ""))
			if user != None:
				if request.method == "GET":
					permissions = ForexClass.getMultipleFromTable("crmUser as a INNER JOIN crmPermissionsByUser as b on a.idCrmUser = b.idCrmUser", "b.idCrmPermissionCat ", " AND b.active = 1 AND a.idCrmUser = " + str(user["ID"]), 6)
					permissions = [permission['idCrmPermissionCat'] for permission in permissions]
					hoy = datetime.datetime.now()
					hoy = hoy - datetime.timedelta(hours=timeInterval)
					hoy = hoy.replace(minute=0, hour=0, second=0)
					requ = {
						"dateType": request.args.get("dateType", "Today"),
						"dateStart": request.args.get("dateStart", str(hoy)[0:10]),
						"dateEnd": request.args.get("dateEnd", str(hoy)[0:10]),
						"country": request.args.get("countries", "ALL"),
						"affiliate": request.args.get("affiliates", "ALL"),
						"status": request.args.get("statuses", "ALL"),
						"businessUnit": request.args.get("businessUnits", "ALL"),
						"receivingBusiness": request.args.get("receivingBusiness", "ALL"),
						"ftds": request.args.get("ftds", 0)
					}
					
					requ = deleteNone(requ)
					if requ["dateType"] == "Today":
						date = " = '"+str(hoy.strftime('%Y-%m-%d'))+"'"
					elif requ["dateType"] == "Yesterday":
						restart = datetime.timedelta(days=1)
						result = hoy - restart
						result = result.strftime('%Y-%m-%d')
						date = " = '"+str(result)+"'"
					elif requ["dateType"] == "This Week":
						start = hoy - datetime.timedelta(days=hoy.weekday())
						end = start + datetime.timedelta(days=6)
						date = " BETWEEN '"+ str(start.strftime('%Y-%m-%d')) +"' AND '"+str(end.strftime('%Y-%m-%d'))+"'"
					elif requ["dateType"] == "Last Week":
						todays = hoy - datetime.timedelta(days=7)
						start = todays - datetime.timedelta(days=todays.weekday())
						end = start + datetime.timedelta(days=6)
						date = " BETWEEN '"+ str(start.strftime('%Y-%m-%d')) +"' AND '"+str(end.strftime('%Y-%m-%d'))+"'"
					elif requ["dateType"] == "This Month":
						monthStart = str(hoy)[0:7] + "-01"
						date = " BETWEEN '"+ monthStart +"' AND '" + str(hoy)[0:10] + "'"
					elif requ["dateType"] == "Last Month":
						real_month = 12 if hoy.month == 1 else hoy.month - 1
						real_year = hoy.year - 1 if hoy.month == 1 else hoy.year
						lastMonthStart = datetime.datetime(real_year, real_month, 1)
						lastMonthEnd = datetime.datetime(hoy.year, hoy.month, 1) - datetime.timedelta(days=1)
						date = " BETWEEN '"+ str(lastMonthStart)[0:10] + "' AND '" + str(lastMonthEnd)[0:10] + "'"
					elif requ["dateType"] == "This Year":
						date = " BETWEEN '"+str(hoy)[0:4]+"-01-01' AND '" + str(hoy)[0:10] + "'"
					elif requ["dateType"] == "Range":
						date = " BETWEEN '"+requ["dateStart"]+"' AND '"+requ["dateEnd"]+"'"
					else:
						date = " = '"+str(hoy)[0:10]+"'"
					
					affiliate = "" if str(requ["affiliate"]) == "ALL" else " AND a.idCrmAffiliate IN (" + remove_char(str(requ["affiliate"])) + ")"
					position = ForexClass.getSingleFromTable("crmUser", "idCrmPositionCat", " AND active = 1 AND idCrmUser = " + str(user["ID"]),6)["idCrmPositionCat"]
					affiliatesByManager = ForexClass.getMultipleFromTable("crmAffiliateByManager", "idCrmAffiliate", " AND active = 1 AND idCrmUser=" + str(user["ID"]), 6)
					affiliatesByManager = [ x["idCrmAffiliate"] for x in affiliatesByManager]
					searchByAffiliate = None
					kpisByManager = None
					if position == 17 and affiliate == "":
						affiliate = " AND a.idCrmAffiliate IN (" + remove_char(str(affiliatesByManager)) +")"
					if position == 18 and 95 in permissions:
						searchByAffiliate = " AND idCrmAffiliate IN (" + remove_char(str(affiliatesByManager)) +")"
						kpisByManager = " AND a.idCrmAffiliate IN (" + remove_char(str(affiliatesByManager)) +")"
						#Filter by Country
					country = "" if str(requ["country"]) == "ALL" else " AND country IN (" + remove_char(str(requ["country"])) + ")"
					countrySumary = "" if str(requ["country"]) == "ALL" else " AND c.country IN (" + remove_char(str(requ["country"])) + ")"
					status = "" if str(requ["status"]) == "ALL" else " AND idCrmCustomerStatusCat IN (" + remove_char(str(requ["status"])) + ")"
					statusUser = "" if str(requ["status"]) == "ALL" else " AND c.idCrmCustomerStatusCat IN (" + remove_char(str(requ["status"])) + ")"
					statusLeads = "" if str(requ["status"]) == "ALL" else " AND a.idCrmCustomerStatusCat IN (" + remove_char(str(requ["status"])) + ")"
					idBusnessUnit = ForexClass.getSingleFromTable("crmUser","idCrmBusinessUnit AS BU"," AND active = 1 AND idCrmUser = " + str(user["ID"]), 6)
					idBusnessUnit = str(idBusnessUnit.get("BU", "")).split(",")
					bussinesUnitWhere = None
					bussinesUnitReciveWhere = None

					if "0" in idBusnessUnit:
						#businessUnit = "" if str(requ["businessUnit"]) == "ALL" else " AND idCrmBusinessUnit IN (" + remove_char(str(requ["businessUnit"])) + ")"
						bussinesUnitWhere = "" if str(requ["businessUnit"]) == "ALL" else " AND a.idCrmBusinessUnit IN (" + remove_char(str(requ["businessUnit"])) + ")"
						bussinesUnitReciveWhere = "" if str(requ["receivingBusiness"]) == "ALL" else " AND a.idBusinessUnitReceives IN (" + remove_char(str(requ["receivingBusiness"])) + ")"

						bussinesUnitTest = "" if str(requ["businessUnit"]) == "ALL" else " AND f.idCrmBusinessUnit IN (" + remove_char(str(requ["businessUnit"])) + ")"

						#businessUnitCustomer = "" if str(requ["businessUnit"]) == "ALL" else " AND c.idCrmBusinessUnit IN (" + remove_char(str(requ["businessUnit"])) + ")"
						businessUnitLeads = "" if str(requ["businessUnit"]) == "ALL" else " AND f.idCrmBusinessUnit IN (" + remove_char(str(requ["businessUnit"])) + ")"
						#businessUnitAffiliates = businessUnitLeads
						businessUnitAffiliates2 = "" if str(requ["businessUnit"]) == "ALL" else " AND idCrmBusinessUnit IN (" + remove_char(str(requ["businessUnit"])) + ")" 
					else:
						availableBussinesUnits = [x for x in idBusnessUnit if x in remove_char(str(requ["businessUnit"])).split(",")]
						if availableBussinesUnits != [] or str(requ["businessUnit"]) == "ALL":
							#businessUnit = " AND a.idCrmBusinessUnit IN (" + ForexClass.lisToChar(idBusnessUnit) + ")" if str(requ["businessUnit"]) == "ALL" else " AND idCrmBusinessUnit IN (" + ForexClass.lisToChar(availableBussinesUnits) + ")"
							bussinesUnitWhere = " AND a.idCrmBusinessUnit IN (" + ForexClass.lisToChar(idBusnessUnit) + ")" if str(requ["businessUnit"]) == "ALL" else " AND a.idCrmBusinessUnit IN (" + ForexClass.lisToChar(availableBussinesUnits) + ")"
							bussinesUnitReciveWhere = "" if str(requ["receivingBusiness"]) == "ALL" else " AND a.idBusinessUnitReceives IN (" + remove_char(str(requ["receivingBusiness"])) + ")"
							bussinesUnitTest = " AND a.idCrmBusinessUnit IN (" + ForexClass.lisToChar(idBusnessUnit) + ")" if str(requ["businessUnit"]) == "ALL" else " AND f.idCrmBusinessUnit IN (" + ForexClass.lisToChar(availableBussinesUnits) + ")"

							#businessUnitCustomer = " AND c.idCrmBusinessUnit IN (" + ForexClass.lisToChar(idBusnessUnit) + ")" if str(requ["businessUnit"]) == "ALL" else " AND c.idCrmBusinessUnit IN (" + ForexClass.lisToChar(availableBussinesUnits) + ")"
							businessUnitLeads = " AND a.idCrmBusinessUnit IN (" + ForexClass.lisToChar(idBusnessUnit) + ")" if str(requ["businessUnit"]) == "ALL" else " AND f.idCrmBusinessUnit IN (" + ForexClass.lisToChar(availableBussinesUnits) + ")"
						else:
							pass
							#businessUnit = businessUnitCustomer = businessUnitLeads = " AND FALSE "
						#businessUnitAffiliates = " AND a.idCrmBusinessUnit IN (" + ForexClass.lisToChar(availableBussinesUnits) + ", 0)" if availableBussinesUnits != [] else " AND a.idCrmBusinessUnit IN (" + ForexClass.lisToChar(idBusnessUnit) + ", 0)"
						businessUnitAffiliates2 = " AND idCrmBusinessUnit IN (" + ForexClass.lisToChar(availableBussinesUnits) + ", 0)" if availableBussinesUnits != [] else " AND idCrmBusinessUnit IN (" + ForexClass.lisToChar(idBusnessUnit) + ", 0)"
					
					ftdsWhere = ""
					ftdsWhereKpis = ""

					if requ['ftds'] == "1" or requ['ftds'] == 1:
						ftdsWhere = " AND c.ftd = 1 " 
						ftdsWhereKpis = " AND a.ftd = 1 "

					where = date + affiliate + country + status
					newWhere = affiliate + countrySumary + statusUser + ftdsWhere
					totalAmountCondition = ""
					check1 = None
					check2 = None

					if not searchByAffiliate:
						affiliateSummary = ForexClass.querySelect(''' SELECT 
																		a.name AS affiliate, 
																		a.idCrmAffiliate AS idAffiliate, 
																		a.remAmount,
																		a.isInternal,
																		d.name as idBusinessUnitReceives,
																		CAST(SUM(IF (c.insertDate, 1, 0)) as SIGNED) as totalLeads,
																		CAST(SUM(IF(c.affiliateactive = 1 AND c.ftd = 1 and (DATE(DATE_SUB(c.affiliateFtdDate, INTERVAL {0} HOUR)) {1} OR DATE(DATE_SUB(c.affiliateFtdDate, INTERVAL {2} HOUR)) {3}) , 1, 0)) AS SIGNED) AS totalAffilitateFtds,
																		0 as totalAmount,
																		CAST(SUM(IF ( (c.affiliateActive = 0 OR c.originalPartner = a.idCrmAffiliate) AND DATE( DATE_SUB(c.ftdDate, INTERVAL {4} HOUR) ) {5}, 1, 0)) AS SIGNED) AS totalCftd 
																	FROM 
																		(SELECT crmId,country, idCrmAffiliate, insertDate, ftdDate, affiliateactive, ftd, originalPartner, idCrmCustomerStatusCat, idCrmBusinessUnit, affiliateFtdDate FROM crmCustomer where active = 1 ) as c 
																	INNER JOIN 
																		(SELECT idCrmAffiliate, name, remAmount, isInternal, idCrmBusinessUnit, idBusinessUnitReceives FROM crmAffiliate where isInternal != 1 and active = 1) as a 
																	ON 
																		c.idCrmAffiliate = a.idCrmAffiliate 
																	INNER JOIN 
																		(SELECT idCrmBusinessUnit, name  FROM crmBusinessUnit where active = 1) as d 
																	ON 
																		d.idCrmBusinessUnit = a.idBusinessUnitReceives  
																	WHERE 
																		(DATE(DATE_SUB(c.insertDate, INTERVAL {6} HOUR)) {7} OR DATE(DATE_SUB(c.ftdDate, INTERVAL {8} HOUR)) {9} OR DATE(DATE_SUB(c.affiliateFtdDate, INTERVAL {10} HOUR)) {11}) 
																	{12} {13} {14}
																	GROUP BY 
																		a.idCrmAffiliate 
																	ORDER BY
																		totalLeads DESC '''.format(timeInterval, date, timeInterval, date, timeInterval, date, timeInterval, date, timeInterval, date, timeInterval, date, newWhere , bussinesUnitWhere, bussinesUnitReciveWhere, ftdsWhere, totalAmountCondition, affiliate ), 6)
						
						#affiliateSummary = ForexClass.querySelect(''' SELECT 
						#												a.name AS affiliate, 
						#												a.idCrmAffiliate AS idAffiliate, 
						#												a.remAmount,
						#												a.isInternal,
						#												d.name as idBusinessUnitReceives,
						#												CAST(SUM(IF (c.insertDate, 1, 0)) as SIGNED) as totalLeads,
						#												CAST(SUM(IF(c.affiliateactive = 1 AND c.ftd = 1 and (DATE(DATE_SUB(c.affiliateFtdDate, INTERVAL {0} HOUR)) {1} OR DATE(DATE_SUB(c.affiliateFtdDate, INTERVAL {2} HOUR)) {3}) , 1, 0)) AS SIGNED) AS totalAffilitateFtds,
						#												CAST(IFNULL(t.amount, 0) as SIGNED) as totalAmount,
						#												CAST(SUM(IF ( (c.affiliateActive = 0 OR c.originalPartner = a.idCrmAffiliate) AND DATE( DATE_SUB(c.ftdDate, INTERVAL {4} HOUR) ) {5}, 1, 0)) AS SIGNED) AS totalCftd 
						#											FROM 
						#												(SELECT crmId,country, idCrmAffiliate, insertDate, ftdDate, affiliateactive, ftd, originalPartner, idCrmCustomerStatusCat, idCrmBusinessUnit, affiliateFtdDate FROM crmCustomer where active = 1 ) as c 
						#											INNER JOIN 
						#												(SELECT idCrmAffiliate, name, remAmount, isInternal, idCrmBusinessUnit, idBusinessUnitReceives FROM crmAffiliate where isInternal != 1 and active = 1) as a 
						#											ON 
						#												c.idCrmAffiliate = a.idCrmAffiliate 
						#											INNER JOIN 
						#												(SELECT idCrmBusinessUnit, name  FROM crmBusinessUnit where active = 1) as d 
						#											ON 
						#												d.idCrmBusinessUnit = a.idBusinessUnitReceives 
						#											LEFT JOIN 
						#												( SELECT a.idCrmAffiliate, a.name, SUM(c.amount) as amount FROM ( SELECT crmId, idCrmAffiliate FROM crmCustomer where active = 1 ) AS b INNER JOIN  ( SELECT crmId, amount FROM crmTransaction where active = 1 AND status = 'APPROVED' AND DATE(DATE_SUB(confirmDate, INTERVAL {4} HOUR)) {5} ) AS c  ON b.crmId = c.crmId INNER JOIN  ( SELECT idCrmAffiliate, name FROM crmAffiliate WHERE active = 1 ) as a ON  a.idCrmAffiliate = b.idCrmAffiliate  GROUP  BY a.idCrmAffiliate ) as t
						#											ON 
						#												t.idCrmAffiliate = a.idCrmAffiliate 
						#											WHERE 
						#												(DATE(DATE_SUB(c.insertDate, INTERVAL {6} HOUR)) {7} OR DATE(DATE_SUB(c.ftdDate, INTERVAL {8} HOUR)) {9} OR DATE(DATE_SUB(c.affiliateFtdDate, INTERVAL {10} HOUR)) {11}) 
						#											{12} {13} {14}
						#											GROUP BY 
						#												a.idCrmAffiliate 
						#											ORDER BY
						#												totalLeads DESC '''.format(timeInterval, date, timeInterval, date, timeInterval, date, timeInterval, date, timeInterval, date, timeInterval, date, newWhere , bussinesUnitWhere, bussinesUnitReciveWhere, ftdsWhere, totalAmountCondition, affiliate ), 6)
						
					if searchByAffiliate:
						affiliateSummary = ForexClass.querySelect(''' SELECT 
																		a.name AS affiliate, 
																		a.idCrmAffiliate AS idAffiliate, 
																		a.remAmount,
																		a.isInternal,
																		d.name as idBusinessUnitReceives,																		
																		CAST(SUM(IF (c.insertDate, 1, 0)) as SIGNED) as totalLeads,
																		CAST(SUM(IF(c.affiliateactive = 1 AND c.ftd = 1 and DATE(DATE_SUB(c.affiliateFtdDate, INTERVAL {0} HOUR)) {1} , 1, 0)) AS SIGNED) AS totalAffilitateFtds,
																		0 as totalAmount,
																		CAST(SUM(IF ( (c.affiliateActive = 0 OR c.originalPartner = a.idCrmAffiliate) AND DATE( DATE_SUB(c.ftdDate, INTERVAL {2} HOUR) ) {3}, 1, 0)) AS SIGNED) AS totalCftd 
																	FROM 
																		(SELECT idCrmAffiliate, name, remAmount, isInternal, idCrmBusinessUnit, idBusinessUnitReceives FROM crmAffiliate where  isInternal != 1 and active = 1 {4}) as a 
																	INNER JOIN 
																		(SELECT idCrmBusinessUnit, name  FROM crmBusinessUnit where active = 1) as d 
																	ON 
																		d.idCrmBusinessUnit = a.idBusinessUnitReceives 
																	LEFT JOIN 
																		(SELECT crmId,country, idCrmAffiliate, insertDate, ftdDate, affiliateactive, ftd, originalPartner, idCrmCustomerStatusCat, idCrmBusinessUnit, affiliateFtdDate FROM crmCustomer where DATE(DATE_SUB(insertDate, INTERVAL {5} HOUR)) {6} and active = 1 OR DATE(DATE_SUB(affiliateFtdDate, INTERVAL {7} HOUR)) {8} and active = 1 ) as c 
																	ON 
																		c.idCrmAffiliate = a.idCrmAffiliate 
																	GROUP BY 
																		a.idCrmAffiliate 
																	ORDER BY
																		totalLeads DESC '''.format(timeInterval, date, timeInterval, date, searchByAffiliate, timeInterval, date, timeInterval, date, timeInterval, date ), 6)
																		
						#affiliateSummary = ForexClass.querySelect(''' SELECT 
						#												a.name AS affiliate, 
						#												a.idCrmAffiliate AS idAffiliate, 
						#												a.remAmount,
						#												a.isInternal,
						#												d.name as idBusinessUnitReceives,																		
						#												CAST(SUM(IF (c.insertDate, 1, 0)) as SIGNED) as totalLeads,
						#												CAST(SUM(IF(c.affiliateactive = 1 AND c.ftd = 1 and DATE(DATE_SUB(c.affiliateFtdDate, INTERVAL {0} HOUR)) {1} , 1, 0)) AS SIGNED) AS totalAffilitateFtds,
						#												CAST(IFNULL(t.amount, 0) as SIGNED) as totalAmount,
						#												CAST(SUM(IF ( (c.affiliateActive = 0 OR c.originalPartner = a.idCrmAffiliate) AND DATE( DATE_SUB(c.ftdDate, INTERVAL {2} HOUR) ) {3}, 1, 0)) AS SIGNED) AS totalCftd 
						#											FROM 
						#												(SELECT idCrmAffiliate, name, remAmount, isInternal, idCrmBusinessUnit, idBusinessUnitReceives FROM crmAffiliate where  isInternal != 1 and active = 1 {4}) as a 
						#											INNER JOIN 
						#												(SELECT idCrmBusinessUnit, name  FROM crmBusinessUnit where active = 1) as d 
						#											ON 
						#												d.idCrmBusinessUnit = a.idBusinessUnitReceives 
						#											INNER JOIN 
						#												(SELECT crmId,country, idCrmAffiliate, insertDate, ftdDate, affiliateactive, ftd, originalPartner, idCrmCustomerStatusCat, idCrmBusinessUnit, affiliateFtdDate FROM crmCustomer where DATE(DATE_SUB(insertDate, INTERVAL {5} HOUR)) {6} and active = 1 OR DATE(DATE_SUB(affiliateFtdDate, INTERVAL {7} HOUR)) {8} and active = 1 ) as c 
						#											ON 
						#												c.idCrmAffiliate = a.idCrmAffiliate 
						#											LEFT JOIN 
						#												( 
						#													SELECT a.idCrmAffiliate, a.name, SUM(c.amount) as amount 
						#													FROM ( SELECT crmId, idCrmAffiliate FROM crmCustomer where active = 1 ) AS b 
						#													INNER JOIN  ( SELECT crmId, amount FROM crmTransaction where active = 1 AND status = 'APPROVED' AND DATE(DATE_SUB(confirmDate, INTERVAL {9} HOUR)) {10} ) AS c  
						#													ON b.crmId = c.crmId 
						#													INNER JOIN  ( SELECT idCrmAffiliate, name FROM crmAffiliate WHERE active = 1 ) as a 
						#													ON  a.idCrmAffiliate = b.idCrmAffiliate  
						#													GROUP  BY a.idCrmAffiliate 
						#												) as t
						#											ON 
						#												t.idCrmAffiliate = a.idCrmAffiliate 
						#											GROUP BY 
						#												a.idCrmAffiliate 
						#											ORDER BY
						#												totalLeads DESC '''.format(timeInterval, date, timeInterval, date, searchByAffiliate, timeInterval, date, timeInterval, date, timeInterval, date ), 6)
																		
					if affiliateSummary:
						for affiliate in affiliateSummary:
							if 88 in permissions and 87 in permissions:
								affiliate["totalFtds"] = round(affiliate["totalAffilitateFtds"] + affiliate["totalCftd"])
							else:
								affiliate["totalFtds"] = round(affiliate["totalAffilitateFtds"])
							if 86 in permissions:
								affiliate["convertion"] = round(affiliate["totalFtds"]*100/catchDiv(affiliate["totalLeads"]),2)
							if searchByAffiliate:
								affiliate["affiliateConvertion"] = 0
								affiliate["lifeTimeValue"] = 0
							else:
								affiliate["affiliateConvertion"] = round(affiliate["totalAffilitateFtds"]*100/catchDiv(affiliate["totalLeads"]),2)
								affiliate["lifeTimeValue"] = round(affiliate["totalAmount"]/catchDiv(affiliate["totalFtds"] if 88 in permissions else affiliate["totalAffilitateFtds"]),2)				
					whereAux = date + country + statusLeads + bussinesUnitTest
			
					if request.args.get("action") == "Information":
						permission = ForexClass.getSingleFromTable("crmPermissionsByUser","idCrmPermissionCat AS permission"," AND active = 1 AND idCrmPermissionCat = 2 AND idCrmUser = " + str(user["ID"]) + "",6)
						if permission != None:
							managerFilter = "" if position != 17 else " AND idCrmAffiliate IN (" + remove_char(str(affiliatesByManager)) +")"
							catalogues = {}
							catalogues["countries"] = ForexClass.getMultipleFromTable("V_countries"," *"," ORDER BY name ASC", 6)
							catalogues["statuses"] = ForexClass.getMultipleFromTable("crmCustomerStatusCat","idCrmStatus AS id, name, 'LEVERATE' AS type"," AND active = 1 ORDER BY name ASC", 6)
							catalogues["antelopes"] = ForexClass.getMultipleFromTable("crmStatusAntelopeCat","id, moisesStatusName as name, 'ANTELOPE' AS type","ORDER BY name ASC", 6)
							catalogues["requftds"] = requ['ftds']
							catalogues["whereftds"] = ftdsWhere
														
							if "0" in idBusnessUnit:
								catalogues["affiliates"] = ForexClass.getMultipleFromTable("crmAffiliate","idCrmAffiliate as id, name"," AND active = 1 " + businessUnitAffiliates2 + managerFilter + " ORDER BY name ASC", 6)
								catalogues["businessUnits"] = ForexClass.getMultipleFromTable("crmBusinessUnit","idCrmBusinessUnit AS id, name, image"," AND active = 1 AND idCrmBusinessUnit > 0 ORDER BY name ASC", 6)
							else:
								catalogues["affiliates"] = ForexClass.getMultipleFromTable("crmAffiliate","idCrmAffiliate as id, name"," AND active = 1 " + managerFilter + " AND idCrmBusinessUnit IN (" + ForexClass.lisToChar(idBusnessUnit) + ", 0) ORDER BY name ASC", 6)
								catalogues["businessUnits"] = ForexClass.getMultipleFromTable("crmBusinessUnit","idCrmBusinessUnit AS id, name, image"," AND active = 1 AND idCrmBusinessUnit IN (" + ForexClass.lisToChar(idBusnessUnit) + ") ORDER BY name ASC", 6)
							catalogues["businessUnitsReceiver"] = ForexClass.getMultipleFromTable("crmBusinessUnit","idCrmBusinessUnit AS id, name"," AND active = 1 AND idCrmBusinessUnit IN (3,6) ORDER BY name ASC",6)
							# kpis
							totalFtdsCondition = " AND a.affiliateActive  = 1" if 88 not in permissions else ""
							kpis = {
								"totalLeads": ForexClass.getSingleFromTable("crmCustomer a INNER JOIN crmAffiliate AS f ON a.idCrmAffiliate = f.idCrmAffiliate","IFNULL(CAST(COUNT(*) AS UNSIGNED),0) AS totalLeads"," AND f.isInternal != 1 AND a.active = 1 AND f.active = 1 AND DATE(DATE_SUB(a.insertDate, INTERVAL "+ str(timeInterval) +" HOUR))" + where + ftdsWhereKpis + businessUnitLeads, 6)['totalLeads'],
								"totalFtds": ForexClass.getSingleFromTable("crmCustomer a INNER JOIN crmAffiliate AS f ON a.idCrmAffiliate = f.idCrmAffiliate","CAST(COUNT(*) AS UNSIGNED) AS totalFtds"," AND f.isInternal != 1 AND a.active = 1 AND f.active = 1 AND ftd = 1 AND DATE(DATE_SUB(ftdDate, INTERVAL "+ str(timeInterval) +" HOUR))" + where + businessUnitLeads + totalFtdsCondition, 6)['totalFtds']
							}
							if searchByAffiliate and kpisByManager:
								kpis = {
									"totalLeads": ForexClass.getSingleFromTable("crmCustomer a INNER JOIN crmAffiliate AS f ON a.idCrmAffiliate = f.idCrmAffiliate","IFNULL(CAST(COUNT(*) AS UNSIGNED),0) AS totalLeads"," AND a.active = 1 AND f.active = 1 AND DATE(DATE_SUB(a.insertDate, INTERVAL "+ str(timeInterval) +" HOUR))" + where + ftdsWhereKpis + kpisByManager , 6)['totalLeads'],
									"totalFtds": ForexClass.getSingleFromTable("crmCustomer a INNER JOIN crmAffiliate AS f ON a.idCrmAffiliate = f.idCrmAffiliate","CAST(COUNT(*) AS UNSIGNED) AS totalFtds"," AND a.active = 1 AND f.active = 1 AND ftd = 1 AND DATE(DATE_SUB(affiliateFtdDate, INTERVAL "+ str(timeInterval) +" HOUR))" + where + kpisByManager + totalFtdsCondition, 6)['totalFtds']
								}
							totalDates = ForexClass.getSingleFromTable("(SELECT DATE_FORMAT(DATE_SUB(insertDate, INTERVAL "+ str(timeInterval) +" HOUR),'%Y-%m-%d') AS a FROM crmCustomer where DATE(DATE_SUB(insertDate, INTERVAL "+ str(timeInterval) +" HOUR)) " + date + " UNION SELECT DATE_FORMAT(DATE_SUB(ftdDate, INTERVAL "+ str(timeInterval) +" HOUR),'%Y-%m-%d') AS a FROM crmCustomer AS a where DATE(DATE_SUB(ftdDate, INTERVAL "+ str(timeInterval) +" HOUR)) 	" + date + ") AUX",
								"COUNT(DISTINCT(a)) AS differentDates",
								"", 6)["differentDates"]
							kpis["convertion"] = round(int(kpis["totalFtds"])*100/catchDiv(int(kpis["totalLeads"])),2)
							kpis["ftdsAverage"] = round(int(kpis["totalFtds"])/catchDiv(int(totalDates)),2)
							kpis["leadsAverage"] = round(int(kpis["totalLeads"])/catchDiv(int(totalDates)),2)
							#Data Assign
							data["kpis"] = kpis
							data["catalogues"] = catalogues
							data["affiliateSummary"] = affiliateSummary
							data['where'] = whereAux
							data['checkFtds'] = ftdsWhereKpis
							data['check'] = businessUnitLeads
							data['check3'] = totalFtdsCondition
							data['review1'] = check1
							data['review2'] = check2
							#Result
							response["result"] = 1
							response["data"] = data
						else:
							response["error"] = "EYHP"
					else:
						response["error"] = "EAMA"
				elif request.method == "PUT":
					permission = ForexClass.getSingleFromTable("crmPermissionsByUser","idCrmPermissionCat AS permission"," AND active = 1 AND idCrmPermissionCat = 11 AND idCrmUser = " + str(user["ID"]) + "",6)
					if permission != None:
						if requ.keys() >= {"customers"}:
							crmIds = []
							for customer in requ["customers"]:
								exist = ForexClass.getSingleFromTable("crmCustomer","crmId", " AND active = 1 AND crmId = '" + str(customer["crmId"]) + "'",6)
								if customer["crmId"] not in crmIds and exist != None:
									updateData = {
										"updateDate": str(datetime.datetime.now()),
										"affiliateFtdDate": str(datetime.datetime.now()),
										"affiliateActive": "1"
									}
									updateWhere = {
										"crmId": customer["crmId"]
									}
									update = ForexClass.updateTable("crmCustomer",updateData,updateWhere,6)
									if update != None:
										crmIds.append(customer["crmId"])
							if len(crmIds) == len(requ["customers"]):
								response["result"] = 1
								response["data"] = crmIds
							elif len(crmIds) > 0:
								response["result"] = 1
								response["data"] = crmIds
								response["error"] = "CWWA"
							else:
								response["error"] = "EUNC"
						else:
							response["error"] = "ENPF"
					else:
						response["error"] = "EYHP"
				else:
					response["error"] = "EMMA"
			else:
				response["error"] = "EISN"
		else:
			response["error"] = "ENPF"
		return response
