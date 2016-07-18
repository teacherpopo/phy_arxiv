	function Keyboard(){
	this.isNumeric = function(e){
		return (e.keyCode >= 48 && e.keyCode <= 57) || (e.keyCode >= 96 && e.keyCode <= 105);
	}
	this.toInt = function(e){
		if (e.keyCode >= 48 && e.keyCode <= 57){return e.keyCode - 48;}
		if (e.keyCode >= 96 && e.keyCode <= 105){return e.keyCode - 96;}
		return 0;
	}

	this.isAlphanumeric = function(e){
		return ((e.keyCode >= 48 && e.keyCode <= 90)|| (e.keyCode >= 93 && e.keyCode <= 111) || (e.keyCode >= 186 && e.keyCode <= 222));
	}

	this.isR = function(e){
		return e.keyCode == 82;
	}

	this.isA = function(e){
		return e.keyCode == 65;
	}

	this.isSpace = function(e){
		return e.keyCode == 32;
	}
	this.isBackSpace = function(e){
		return e.keyCode == 8;
	}
	this.isEnter = function(e){
		return e.keyCode == 13;
	}
	this.isUp = function(e){
		return e.keyCode == 38;
	}
	this.isDown = function(e){
		return e.keyCode == 40;
	}
	this.isLeft = function(e){
		return e.keyCode == 37;
	}
	this.isRight = function(e){
		return e.keyCode == 39;
	}
}

var keyboard = new Keyboard();
var dummy = $("#dummy");


function AjaxQueue(filterObj){
	this.queue = [];
	this.filterObj = filterObj;
	this.QUICKBLOCK = 75000;
	this.isPopping = false;

	// parsedClone must be cloned
	this.Push = function(parsedClone, metaClone, cache = false, quickIndex = 0, querySize = -1){
		if (cache){
			this.queue.push({"cache": cache, "parsed":parsedClone, "meta":metaClone});
		}else {
			for (var q = quickIndex; q < querySize; q += this.QUICKBLOCK){
				this.queue.push({"cache": cache, "parsed":parsedClone, "meta":metaClone, "quickIndex":q, "querySize":querySize});
			}
		}
		this.Pop();
	}

	this.Pop = function(){
		if (this.queue.length == 0){return;}
		if (this.isPopping){return;}
		this.isPopping = true;
		var ajaxCall = this.queue.shift();

		var cache = ajaxCall["cache"];
		var parsed = ajaxCall["parsed"];
		var meta = ajaxCall["meta"];

		if (this.filterObj.parsedIsEmpty(parsed)){
			this.filterObj.clearResponse();
			this.filterObj.displaySearch();
			this.isPopping = false;
			this.Pop();
		}else if (!this.filterObj.sameDict(parsed, this.filterObj.parsed) || !this.filterObj.sameDict(meta, this.filterObj.meta)){
			this.isPopping = false;
			this.Pop();
		}else{
			if (cache){
				$.ajax({
						url: "/oai/cache",
						type: "GET",
						data: $.extend($.extend({}, parsed), meta),
						context: {"filterObj":this.filterObj, "parsed":parsed, "meta":meta},
						success: function(data){
							var response = JSON.parse(data);
							var querySize = response["header"]["querySize"]
							var parsed = this["parsed"];
							var meta = this["meta"];
							var filterObj = this["filterObj"];
							filterObj.init = 0;
							filterObj.selection = -1;
							filterObj.isFocused = false;
							filterObj.header["time"] = response["header"]["time"];
							filterObj.body = response["body"];
							if (filterObj.body.length > 0 && filterObj.selection < 0){filterObj.selection = 0;}
							filterObj.displaySearch();
							filterObj.aQueue.isPopping = false;
							filterObj.aQueue.Push(parsedClone = $.extend({},parsed), metaClone = $.extend({}, meta), cache = false, quickIndex = 0, querySize = parseInt(querySize));

						}
					})
			}else{
				var quickIndex = ajaxCall["quickIndex"];
				var querySize = ajaxCall["querySize"];
				$.ajax({
					url: "/oai/filter",
					type: "GET",
					data: $.extend($.extend({"quickIndex":quickIndex}, parsed), meta),
					context: {"quickIndex":quickIndex, "filterObj":this.filterObj},
					success: function(data){
						var response = JSON.parse(data);
						var quickIndex = this["quickIndex"];
						var filterObj = this["filterObj"];

						filterObj.header["time"] += response["header"]["time"];
						$.merge(filterObj.body, response["body"]);
						if (filterObj.body.length > 0 && filterObj.selection < 0){filterObj.selection = 0;}
						filterObj.displaySearch();
						filterObj.aQueue.isPopping = false;
						filterObj.aQueue.Pop();
					}
				})
			}
		}
	}
}

function Filter(filterId, displayId){
	this.filter = $("#"+filterId);
	this.filterStr = "";
	this.header = {"time":0, "querySize":-1};
	this.body = [];
	this.parsed = {"abstract":"", "title":"", "authors":"", "cate":""};	
	this.minLength = {"abstract":3, "title":3, "authors":2, "cate":2};	
	this.parsedLast = $.extend({}, this.parsed);
	this.meta = {"since":"", "until":""};
	this.metaLast = $.extend({}, this.meta);
	this.isFocused = false;
	this.tapIndex = 0;
	this.history = [];
	this.aQueue = new AjaxQueue(this);
	this.maxAuthorsLength = 10;

	this.filter[0].parent = this;
	this.filter.bind("keyup", function(e){
		if ((keyboard.isAlphanumeric(e) || keyboard.isBackSpace(e) || keyboard.isSpace(e) || keyboard.isEnter(e)) && !(e.ctrlKey && keyboard.isEnter(e))){
			this.parent.doSearch();
		}
	});

	this.filter.bind("focus", function(){
		this.parent.filter.css("background-color", "#A5CBFF");
		var displayAgain = false;
		if (this.parent.isFocused){displayAgain = true;}
		this.parent.isFocused = false;
		if (displayAgain){this.parent.displaySearch();}
	})

	this.filter.bind("blur", function(){
		this.parent.filter.css("background-color", "white");
		if (this.parent.body.length == 0){return;}
	});
	this.filter.focus();
		

	this.N = 5;
	this.init = 0;
	this.selection = -1;
	this.isFocused = false;
	this.display = $("#"+displayId);
	this.display[0].parent = this;
	this.highlightColor = "#A5CBFF";

	$(document)[0].filterObj = this;

	this.headerDisplay = $("<div>");
	this.headerDisplay.hide();
	this.count = $("<span>", {html: 0});
	this.time = $("<span>", {html: 0});
	this.query = $("<div>");
	this.query[0].id = "queryDisplay";
	//this.headerDisplay.append("We found ").append(this.count).append(" results in ").append(this.time).append(" seconds.<br><br>");
	this.headerDisplay.append("We found ").append(this.count).append(" results.<br><br>");
	this.display.append(this.headerDisplay).append(this.query);

	this.blockSpam = false;

	$(document).bind("keydown", function(e){
		if (this.blockSpam){return;}
		else{
			this.blockSpam = true;
			setTimeout(function(filterObj){filterObj.blockSpam = false;}, 50, this);
		}
		var parent = this.filterObj;
		var filter = parent.filter;
		if (e.ctrlKey && keyboard.isEnter(e)){
			
			if (filter.is(":focus")){
				if (parent.canSearch() && parent.body.length > 0){
					filter.blur();
					parent.isFocused = true;
					parent.displaySearch();
				}
			}else{
				filter.focus();
				parent.isFocused = false;
				parent.displaySearch();
			}
		}else{
			if (parent.isFocused){
				if (keyboard.isDown(e)){
					parent.moveSelection(1);
				}else if (keyboard.isUp(e)){
					parent.moveSelection(-1);
				}else if (keyboard.isLeft(e)){
					parent.moveSelection(-parent.N);
				}else if (keyboard.isRight(e)){
					parent.moveSelection(parent.N);
				}else if (keyboard.isNumeric(e) || keyboard.isR(e)){
					parent.rate(parent.selection, e);
				}else if (keyboard.isA(e)){
					parent.archive(parent.selection);
				}
			}
		}

	});

	$(document).bind("click", function(){
		var parent = this.filterObj;
		var displayAgain = false;
		if (!parent.query.is(":hover")){
			if (parent.isFocused){displayAgain = true;}
			parent.isFocused = false;
			if (displayAgain){parent.displaySearch();}
		}
		
	})

	this.sameDict = function(parsed1, parsed2){
		for (var key in parsed1){
			if (parsed1[key] != parsed2[key]){
				return false;}
		}
		return true;
	}

	this.sameSearch = function(){
		return this.sameDict(this.parsed, this.parsedLast) && this.sameDict(this.meta, this.metaLast);
	}


	this.emptyParsed = function(){
		for (var key in this.parsed){
			this.parsed[key] = "";
		}
	}

	this.emptyMeta = function(){
		for (var key in this.meta){
			this.meta[key] = "";
		}
	}
	
	this.getList = function(name){
		if (this.parsed[name] == "" || this.parsed[name] == ","){
			return [];
		}
		return this.parsed[name].split(',');;
	}

	this.reduceOnce = function(name){
		var items = this.getList(name);
		this.parsed[name] = "";
		for (var i = 0; i < items.length; i++){
			if (items[i].length >= this.minLength[name]){
				this.parsed[name] += items[i] + ",";
			}
		}
	}

	this.reduce = function(){
		for (var key in this.parsed){
			this.reduceOnce(key);
		}
	}

	this.shrink = function(command){
		var items = command.split(',');
		var shrunk = "";
		for (var i = 0; i < items.length; i++){
			shrunk += items[i].trim() + ","
		}

		return shrunk;
	}

	this.isDigits = function(str){
		for (var i = 0; i < str.length; i++){
			if (!$.inArray(str[i], ['\0','1','2','3','4','5','6','7','8','9'])){return false;}
		}
		return true;
	}

	this.isLeap = function(year){
		if (year % 100 == 0){
			if (year % 400 == 0){return true;}
			else {return false;}
		}else{
			if (year % 4 == 0){return true;}
			else {return false;}
		}
	}


	this.isValidDateStr = function(yearStr, monthStr, dayStr){
		if (yearStr.length != 4 || monthStr.length == 0 || monthStr.length > 2 || dayStr.length == 0 || dayStr.length > 2){return false;}
		if (!this.isDigits(yearStr) || !this.isDigits(monthStr) || !this.isDigits(dayStr)){return false;}
		var year = parseInt(yearStr);
		var month = parseInt(monthStr);
		var day = parseInt(dayStr);
		
		if (month > 12 || month < 1){return false;}
		if (month == 2){
			if (this.isLeap(year)){
				if (1 <= day && day <= 29){return true;}
				else {return false;}
			}else{
				if (1 <= day && day <= 28){return true;}
				else {return false;}
			}
		}

		if ($.inArray(month, [1,3,5,7,8,10,12])){
			if (1 <= day && day <= 31){return true;}
			else {return false;}
		}else{
			if (1 <= day && day <= 30){return true;}
			else {return false;}
		}
	}

	this.getDateFromStr = function(str, directive){
		if (str == ""){return "";}
		var command = str.split(' ')[0];
		var residue = str.substring(command.length, str.length).trim();

		var today = new Date();
		var year = today.getFullYear();
		var month = today.getMonth();
		var date = today.getDate();
		var day = today.getDay();

		if (command == "today"){
			if (residue != ""){return "";}
			return year.toString() + "-" + (month+1).toString() + "-"+date.toString();
		}else if (command == "this"){
			if (residue.split(' ').length != 1){return "";}
			if (directive == "until" && (residue == "month" || residue == "year" || residue == "week")){
				return year.toString() + "-" + (month+1).toString() + "-"+date.toString();}
			else if (directive == "since"){
				if (residue == "month"){
					return year.toString() + "-" + (month+1).toString() + "-01";
				}else if(residue == "year"){
					return year.toString() + "-01-01";
				}else if(residue == "week"){
					var tmpDate = new Date();
					tmpDate.setDate(date - day);
					return tmpDate.getFullYear().toString() +"-" + (tmpDate.getMonth()+1).toString() + "-"+tmpDate.getDate().toString();
				}else{
					return "";
				}
			}else{return "";}
		}else if (command == "last" || command == "prev" || command == "previous"){
			if (residue.split(' ').length != 1){return "";}
			if (directive == "until"){
				if (residue == "month"){
					var tmpDate = new Date();
					tmpDate.setDate(0);
					return tmpDate.getFullYear().toString() +"-" + (tmpDate.getMonth()+1).toString() + "-"+tmpDate.getDate().toString();
				}else if (residue == "year"){
					return (year-1).toString() + "-12-31";
				}else if (residue == "week"){
					var tmpDate = new Date();
					tmpDate.setDate(date - day - 1);
					return tmpDate.getFullYear().toString() +"-" + (tmpDate.getMonth()+1).toString() + "-"+tmpDate.getDate().toString();
				}else{
					return "";
				}
			}else if (directive == "since"){
				if (residue == "month"){
					if (month > 0){return year.toString() + "-" + month.toString() + "-01";}
					else {return (year-1).toString() + "-12-01";}
				}else if(residue == "year"){
					return (year-1).toString() + "-01-01";
				}else if(residue == "week"){
					var tmpDate = new Date();
					tmpDate.setDate(date - day - 7);
					return tmpDate.getFullYear().toString() +"-" + (tmpDate.getMonth()+1).toString() + "-"+tmpDate.getDate().toString();
				}else{
					return "";
				}
			}else{return "";}
		}else{
			//if (command == ""){return "";}
			if (str.indexOf('-') > -1 && str.indexOf('/') > -1){return "";}
			var numbers = command.split(/-|\//);
			if (numbers.length != 3) {return "";}
			var yearStr = numbers[0].trim();
			var monthStr = numbers[1].trim();
			var dayStr = numbers[2].trim();
			if (this.isValidDateStr(yearStr, monthStr, dayStr)){return yearStr + "-" + monthStr + "-" + dayStr;}
			else {return "";}
		}
	}

	this.compareDateStr = function(date1, date2, directive){
		if (date1 == ""){return date2;}
		else if (date2 == ""){return date1;}

		var numbers = [date1.split(/-|\//), date2.split(/-|\//)];
		var year = [parseInt(numbers[0][0]), parseInt(numbers[1][0])];
		var month = [parseInt(numbers[0][1]), parseInt(numbers[1][1])];
		var date = [parseInt(numbers[0][2]), parseInt(numbers[1][2])];

		var earlier = date1;
		var later = date2;

		if (year[0] > year[1] || month[0] > month[1] || date[0] > date[1]){
			earlier = date2;
			later = date1;
		}

		if (directive == "earlier"){return earlier;}
		else if (directive == "later"){return later;}
		else {return date1;}

	}

	this.parseFilterStr = function(){
		this.emptyParsed();
		this.emptyMeta();
		var filterLines = this.filterStr.split('\n');
		for (var l = 0; l < filterLines.length; l++){
			var residue = filterLines[l].trim();
			if (residue == ''){continue;}
			var command = residue.split(' ')[0];
			residue = residue.substring(command.length, residue.length).trim();
			if (command in this.parsed){
				var subCommand = residue.split(' ')[0];
				var subSubCommand = residue.substring(subCommand.length, residue.length).trim();

				if (subCommand == "like"){
					subSubCommand = this.shrink(subSubCommand);
					this.parsed[command] += subSubCommand;
				}
			}else if (command in this.meta){
				//this.meta[command] = this.getDateFromStr(residue, command);
				var newDate = this.getDateFromStr(residue, command);
				if (command == "since"){this.meta[command] = this.compareDateStr(this.meta[command], newDate, "later");}
				else if (command == "until"){this.meta[command] = this.compareDateStr(this.meta[command], newDate, "earlier");}

				//dummy.append(this.meta["since"]+"/"+this.meta["until"]+"<p><p>");
			}
		}
		this.reduce();
	}

	this.parsedIsEmpty = function(parsed){
		for (var key in this.parsed){
			if (parsed[key].length != 0){return false;}
		}
		return true;
	}

	this.canSearch = function(){
		return !this.parsedIsEmpty(this.parsed);
	}

	this.clearResponse = function(){
		this.header["time"] = 0;
		this.body = [];
	}

	this.doSearch = function(){
		this.filterStr = this.filter.val();
		this.parseFilterStr();

		if (this.sameSearch()){return;}
		else {this.parsedLast = $.extend({}, this.parsed); this.metaLast = $.extend({}, this.meta);}
		this.aQueue.Push(parsedClone = $.extend({}, this.parsed), metaClone = $.extend({}, this.meta), cache = true);
	}

	this.avoidNull = function(element, replacement){
		if (element == null){
			return replacement;
		}else{
			return element;
		}
	}

	this.elementHTML = function(index){
		var jsonElement = this.body[index];
		var identifier = this.avoidNull(jsonElement["identifier"], "[no identifier]");
		var title = this.avoidNull(jsonElement["title"], "[no title]");
		var authors = this.avoidNull(JSON.parse(jsonElement["authors"]), []);
		var rating = jsonElement["rating"];
		var archived = jsonElement["archived"];
		var printHTML = "<font color=\"#FF0000\">" +(index+1)+"</font>" + "  <b>"+identifier + "</b>";
		if (rating != null){
			printHTML += " <font color=\"#BF00FF\">r" + rating.toString() + "</font>";
		}
		if (archived){
			printHTML += " <font color=\"#FFC300\">a</font>";
		}

		printHTML += "<br>";
		printHTML += title + "<br>";

		for (var a = 0; a < authors.length && a < this.maxAuthorsLength; a++){
			var author = authors[a];
			var keyname = author["keyname"];
			var forenames = author["forenames"];
			printHTML += "<i>" + forenames + " " + keyname + "</i>";
			if (a < authors.length - 1 && a < this.maxAuthorsLength - 1){
				printHTML += ", ";
			}
		}

		if (this.maxAuthorsLength < authors.length){printHTML += ", et al.";}

		return printHTML;
	}

	this.displayHeader = function(){
		this.headerDisplay.show();
		this.count.html(this.body.length);
		this.time.html(this.header["time"].toPrecision(4));
	}

	this.displaySearch = function(){
		//dummy.append("1");
		if (!this.canSearch()){
			this.headerDisplay.hide();
		}else{
			this.displayHeader();
		}

		this.query.empty();
		for (var i = this.init; i < this.init + this.N && i < this.body.length; i++){
			var tagElement = $("<div>", {html: this.elementHTML(i)});
			tagElement[0].parent = this;
			tagElement[0].index = i;
			tagElement[0].id = "tagElement-" + i.toString();
			tagElement[0].identifier = this.body[i]["identifier"];
			tagElement.bind("click", function(){
				this.parent.isFocused = true;
				this.parent.selection = this.index;
				tagElement.css("background-color", this.highlightColor);
				this.parent.displaySearch();
			});
			if (this.isFocused && this.selection == i){
				tagElement.css("background-color", this.highlightColor);
			}
			this.query.append(tagElement);
		}
		//MathJax.Hub.Queue(["Typeset", MathJax.Hub, this.query[0].id]);
	}

	this.goTo = function(init){
		this.init = init;
		this.displaySearch();
	}

	this.moveSelection = function(step){
		if (!this.isFocused || (this.selection == 0 && step < 0) || (this.selection == this.body.length - 1 && step > 0)) {return;}
		if (step > 0 && (this.selection + step >= this.body.length)){
			this.selection = this.body.length - 1;
			this.goTo(Math.max(0,this.body.length - this.N));
		}else if (step < 0 && (this.selection < -step)){
			this.selection = 0;
			this.goTo(0);
		}else{
			this.selection += step;
			if (this.init <= this.selection && this.selection < this.init + this.N){
				this.displaySearch();
			}else{
				var initTmp = this.init + step;
				if (initTmp >= this.body.length - this.N){
					this.goTo(this.body.length - this.N);
				}else if (initTmp < 0){
					this.goTo(0);
				}else{
					this.goTo(this.init + step);
				}
			}
		}
	}

	this.updateArchive = function(identifier){
		for (var i = 0; i < this.body.length; i++){
			if (this.body[i]["identifier"] == identifier){this.body[i]["archived"] = (this.body[i]["archived"]+1)%2;}
		}
	}

	this.archive = function(index){
		var tagElement = $("#tagElement-" + index.toString());
		var identifier = tagElement[0].identifier;
		this.updateArchive(identifier);
		this.displaySearch();
		$.ajax({
			url: "/oai/archive",
			type: "GET",
			data: {"identifier":identifier},
			success: function(data){
				// Display error message, if any
			}
		})
	}


	this.updateRatings = function(identifier, rating){
		if (rating < 0){rating = null;}
		for (var i = 0; i < this.body.length; i++){
			if (this.body[i]["identifier"] == identifier){this.body[i]["rating"] = rating;}
		}
	}

	this.rate = function(index, e){
		var tagElement = $("#tagElement-" + index.toString());
		var identifier = tagElement[0].identifier;
		var rating = -1;
		if (keyboard.isNumeric(e)){
			rating = keyboard.toInt(e);
		}

		this.updateRatings(identifier, rating);
		this.displaySearch();
		// Make ajax call to /oai/rate
		$.ajax({
			url: "/oai/rate",
			type: "GET",
			data: {"identifier":identifier, "rating":rating.toString()},
			context: this,
			success: function(data){
				// Display error message, if any
			}
		})
	}
}
