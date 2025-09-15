// Minimal navbar toggler without bootstrap.js
document.addEventListener('DOMContentLoaded', function () {
	const toggler = document.querySelector('[data-bs-toggle="collapse"]');
	const target = document.querySelector('#navbarNav');
	if (toggler && target) {
		toggler.addEventListener('click', function () {
			target.classList.toggle('show');
			const expanded = toggler.getAttribute('aria-expanded') === 'true';
			toggler.setAttribute('aria-expanded', (!expanded).toString());
		});
	}

	// Active link highlight in navbar based on current path
	const path = window.location.pathname;
	document.querySelectorAll('.navbar .nav-link').forEach(function (link) {
		if (link.getAttribute('href') === path) {
			link.classList.add('active');
		}
	});

	// Dark mode toggle (press "D" or add a button later)
	try {
		const savedTheme = localStorage.getItem('theme');
		if (savedTheme === 'dark') {
			document.body.classList.add('dark');
		}
	} catch (e) { console.error(e); }

	// Sync aria-pressed on theme toggle with saved theme
	(function(){
		const btn = document.getElementById('themeToggle');
		if (!btn) return;
		const isDark = document.body.classList.contains('dark');
		btn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
	})();

	// Online/Offline badge updater
	(function(){
		const badge = document.getElementById('offlineBadge');
		if (!badge) return;
		function update() {
			const online = navigator.onLine;
			badge.textContent = online ? 'En ligne' : 'Hors-ligne';
			badge.classList.toggle('bg-success', online);
			badge.classList.toggle('bg-danger', !online);
		}
		window.addEventListener('online', update);
		window.addEventListener('offline', update);
		update();
	})();

	// Print header datetime
	(function(){
		const el = document.getElementById('printDatetime');
		if (!el) return;
		try {
			const now = new Date();
			const fmt = now.toLocaleString();
			el.textContent = 'Imprimé le ' + fmt;
		} catch(e) { console.error(e); }
	})();

	document.addEventListener('keydown', function (e) {
		if (e.key.toLowerCase() === 'd') {
			document.body.classList.toggle('dark');
			try {
				localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
			} catch (e) { console.error(e); }
		}
	});

	const btn = document.getElementById('themeToggle');
	if (btn) {
		btn.addEventListener('click', function () {
			document.body.classList.toggle('dark');
			const pressed = btn.getAttribute('aria-pressed') === 'true';
			btn.setAttribute('aria-pressed', (!pressed).toString());
			try {
				localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
			} catch (e) { console.error(e); }
		});
	}

	// Global sparkline renderer (any canvas.spark on any page)
	function renderSpark(el) {
		try {
			const ctx = el.getContext('2d');
			const points = (el.getAttribute('data-points') || '').split(',').map(function (v) { return parseFloat(v) || 0; });
			if (!points.length) return;
			new Chart(ctx, {
				type: 'line',
				data: {
					labels: points.map(function (_, i) { return i + 1; }),
					datasets: [{ data: points, borderColor: '#ff7900', backgroundColor: 'rgba(255,121,0,0.15)', fill: true, tension: 0.35, borderWidth: 2, pointRadius: 0 }]
				},
				options: { responsive: false, plugins: { legend: { display: false }, tooltip: { enabled: false } }, scales: { x: { display: false }, y: { display: false } } }
			});
		} catch (e) { console.error(e); }
	}
	document.querySelectorAll('canvas.spark').forEach(renderSpark);

	// Interfaces page enhancements: search, filter, sort
	(function enhanceInterfaces() {
		const table = document.getElementById('ifTable');
		if (!table) return;
		const tbody = table.querySelector('tbody');
		const rows = Array.from(tbody.querySelectorAll('tr'));
		const search = document.getElementById('ifSearch');
		const status = document.getElementById('ifStatus');
		const exportBtn = document.getElementById('ifExport');
		const resetBtn = document.getElementById('ifReset');

		function normalize(text) { return (text || '').toString().toLowerCase(); }
		function getStateBadgeText(cell) {
			const t = cell.textContent.trim().toUpperCase();
			if (t.includes('UP')) return 'UP';
			if (t.includes('DOWN')) return 'DOWN';
			return t;
		}
		function applyFilters() {
			const q = normalize(search?.value);
			const st = status?.value || '';
			let visible = 0;
			rows.forEach(function (tr) {
				const cols = tr.children;
				const equip = normalize(cols[0].textContent);
				const iface = normalize(cols[1].textContent);
				const state = getStateBadgeText(cols[2]);
				const matchText = !q || equip.includes(q) || iface.includes(q);
				const matchState = !st || state === st;
				const show = (matchText && matchState);
				tr.style.display = show ? '' : 'none';
				if (show) visible++;

				// Threshold badges: high throughput or errors
				const thrCell = cols[3]; const errCell = cols[4];
				if (thrCell) {
					const thr = parseFloat(thrCell.querySelector('.num')?.textContent) || 0;
					thrCell.classList.toggle('table-warning', thr >= 900);
				}
				if (errCell) {
					const errs = parseFloat(errCell.querySelector('.num')?.textContent) || 0;
					errCell.classList.toggle('table-danger', errs >= 10);
				}
			});
			const badge = document.getElementById('ifCount');
			if (badge) badge.textContent = visible + '/' + rows.length;
		}
		if (search) search.addEventListener('input', applyFilters);
		if (status) status.addEventListener('change', applyFilters);
		applyFilters();

		// Sorting by clicking on headers
		const sortDir = {};
		table.querySelectorAll('thead th[data-sort]').forEach(function (th, idx) {
			th.style.cursor = 'pointer';
			th.addEventListener('click', function () {
				const key = th.getAttribute('data-sort');
				sortDir[key] = sortDir[key] === 'asc' ? 'desc' : 'asc';
				const dir = sortDir[key];
		// aria-sort update
		table.querySelectorAll('thead th[data-sort]').forEach(function (oth) { oth.setAttribute('aria-sort', 'none'); });
		th.setAttribute('aria-sort', dir);
				rows.sort(function (a, b) {
					function cellVal(tr) {
						if (key === 'equip') return tr.children[0].textContent.trim();
						if (key === 'iface') return tr.children[1].textContent.trim();
						if (key === 'state') return getStateBadgeText(tr.children[2]);
						if (key === 'throughput') return parseFloat(tr.children[3].querySelector('.num').textContent) || 0;
						if (key === 'errors') return parseFloat(tr.children[4].querySelector('.num').textContent) || 0;
						return '';
					}
					var va = cellVal(a), vb = cellVal(b);
					if (typeof va === 'number' && typeof vb === 'number') {
						return dir === 'asc' ? va - vb : vb - va;
					}
					return dir === 'asc' ? String(va).localeCompare(String(vb)) : String(vb).localeCompare(String(va));
				});
				rows.forEach(function (tr) { tbody.appendChild(tr); });
			});
		});

		// Reset filters
		function resetFilters() {
			if (search) search.value = '';
			if (status) status.value = '';
			applyFilters();
			// Reset aria-sort
			table.querySelectorAll('thead th[data-sort]').forEach(function (th) { th.setAttribute('aria-sort', 'none'); });
		}
		if (resetBtn) resetBtn.addEventListener('click', function (e) { e.preventDefault(); resetFilters(); });

		// CSV export
		function toCSV(text) {
			return '"' + text.replace(/"/g, '""') + '"';
		}
		function exportCSV() {
			var lines = [];
			var headers = Array.from(table.querySelectorAll('thead th')).map(function (th) { return th.textContent.trim(); });
			lines.push(headers.join(','));
			rows.forEach(function (tr) {
				if (tr.style.display === 'none') return;
				var cells = Array.from(tr.children).map(function (td, i) {
					if (i === 3 || i === 4) {
						var n = td.querySelector('.num');
						return n ? n.textContent.trim() : td.textContent.trim();
					}
					return td.textContent.trim();
				});
				lines.push(cells.map(toCSV).join(','));
			});
			var blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
			var url = URL.createObjectURL(blob);
			var a = document.createElement('a');
			a.href = url; a.download = 'interfaces.csv'; a.click();
			setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
		}
		if (exportBtn) exportBtn.addEventListener('click', exportCSV);

	})();

	// Dashboard charts (health donut + weekly traffic) rendered if elements exist
	(function dashboardCharts(){
		var donut = document.getElementById('healthDonut');
		if (donut) {
			try {
				var dctx = donut.getContext('2d');
				new Chart(dctx, {
					type: 'doughnut',
					data: { labels: ['Sain','Risque'], datasets: [{ data: [72, 28], backgroundColor: ['#ff7900','rgba(255,121,0,0.2)'], borderWidth: 0 }] },
					options: { plugins: { legend: { display: false } }, cutout: '70%' }
				});
			} catch (e) {}
		}
		var traffic = document.getElementById('networkChart');
		if (traffic) {
			try {
				var tctx = traffic.getContext('2d');
				new Chart(tctx, {
					type: 'line',
					data: { labels: ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'], datasets: [{ data: [12,19,13,18,16,21,24], borderColor: '#ff7900', backgroundColor: 'rgba(255,121,0,0.2)', fill: true, tension: 0.35, pointRadius: 0, borderWidth: 2 }] },
					options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
				});
			} catch (e) {}
		}
	})();
});
