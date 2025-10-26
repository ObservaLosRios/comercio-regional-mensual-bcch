const FIGURE_SPECS = {
	ventasMensuales: {
		dataKey: 'ventasMensuales',
		target: 'ventas-mensuales-chart',
		highlightRegion: 'Metropolitana',
		hoverFallback: '<b>%{fullData.name}</b><br>%{x|%Y-%m}: %{y:,.0f} MM CLP<extra></extra>',
		config: {
			toImageButtonOptions: {
				format: 'png',
				filename: 'ventas-mensuales-por-region',
				scale: 2
			}
		}
	},
	variacionInteranual: {
		dataKey: 'variacionInteranual',
		target: 'variacion-interanual-chart',
		highlightRegion: 'Metropolitana',
		hoverFallback: '<b>%{fullData.name}</b><br>%{x|%Y-%m}: %{y:.1f}%<extra></extra>',
		config: {
			toImageButtonOptions: {
				format: 'png',
				filename: 'variacion-interanual-ventas-regionales',
				scale: 2
			}
		}
	}
};

const FIGURE_DATA = window.FIGURE_DATA || {};

const deepClone = (value) =>
	typeof structuredClone === 'function'
		? structuredClone(value)
		: JSON.parse(JSON.stringify(value));

function computePlotDimensions(container) {
	const rect = container.getBoundingClientRect();
	const parentRect = container.parentElement
		? container.parentElement.getBoundingClientRect()
		: { width: 0, height: 0 };
	const computed = window.getComputedStyle(container);

	const width = Math.max(rect.width, parentRect.width, parseFloat(computed.width) || 0);
	const height = Math.max(rect.height, parseFloat(computed.height) || 0);

	return {
		width: Number.isFinite(width) ? Math.round(width) : 0,
		height: Number.isFinite(height) ? Math.round(height) : 0
	};
}

async function loadFigure(dataKey) {
	const figure = FIGURE_DATA[dataKey];
	if (!figure) {
		throw new Error(`No se encontró la figura con clave "${dataKey}"`);
	}
	return deepClone(figure);
}

function applyEconomistTouches(layout) {
	const clone = deepClone(layout);
	const underlineColor = '#b91c1c';
	const underlineHeight = 2;

	clone.annotations = clone.annotations || [];
	const sourceNote = clone.annotations.find(
		(annotation) => annotation.text && annotation.text.includes('Banco Central de Chile')
	);
	if (sourceNote) {
		sourceNote.y = -0.2;
	}

	clone.shapes = clone.shapes || [];
	const underline = clone.shapes.find((shape) => shape.type === 'line');
	if (underline) {
		underline.y0 = 1.08;
		underline.y1 = 1.08;
		underline.line.color = underlineColor;
		underline.line.width = underlineHeight;
	}

	clone.margin = clone.margin || {};
	clone.margin.r = 140;
	clone.margin.t = 90;

	clone.legend = clone.legend || {};
	clone.legend.title = { text: 'Región' };
	clone.legend.bgcolor = 'rgba(255, 255, 255, 0.75)';
	clone.legend.font = { ...(clone.legend.font || {}), family: 'Georgia, serif' };

	clone.hovermode = 'x unified';
	clone.hoverlabel = clone.hoverlabel || {};
	clone.hoverlabel.bgcolor = 'rgba(255, 255, 255, 0.9)';
	clone.hoverlabel.font = {
		...(clone.hoverlabel.font || {}),
		family: 'Georgia, serif',
		size: 12,
		color: '#111827'
	};
	clone.hoverlabel.align = 'left';
	clone.hoverlabel.bordercolor = 'rgba(0, 0, 0, 0.05)';
	clone.hoverlabel.namelength = -1;

	clone.xaxis = clone.xaxis || {};
	clone.xaxis.showspikes = true;
	clone.xaxis.spikemode = 'across';
	clone.xaxis.spikesnap = 'cursor';
	clone.xaxis.spikecolor = 'rgba(100, 116, 139, 0.35)';
	clone.xaxis.spikethickness = 1.2;
	clone.xaxis.spikedash = 'solid';
	clone.xaxis.showline = true;
	clone.xaxis.linecolor = 'rgba(148, 163, 184, 0.4)';
	clone.xaxis.linewidth = 1;

	clone.yaxis = clone.yaxis || {};
	clone.yaxis.showspikes = false;

	return clone;
}

function prepareRegionalTraces(traces, options = {}) {
	const highlightRegion = options.highlightRegion || 'Metropolitana';
	const hoverFallback = options.hoverFallback;

	return traces.map((trace) => {
		const clone = deepClone(trace);

		if (clone.name === 'Santiago') {
			clone.name = highlightRegion;
			clone.legendgroup = highlightRegion;
		}

		if (clone.name === highlightRegion) {
			clone.visible = 'legendonly';
		} else if (clone.visible === 'legendonly') {
			delete clone.visible;
		}

		if (!clone.hovertemplate && hoverFallback) {
			clone.hovertemplate = hoverFallback;
		}

		return clone;
	});
}

async function renderChart(spec) {
	const container = document.getElementById(spec.target);
	if (!container) {
		return;
	}

	const section = container.closest('.section');
	const needsTemporaryReveal = section && !section.classList.contains('active');
	let sectionStyles;
	let containerStyles;

	if (needsTemporaryReveal) {
		sectionStyles = {
			display: section.style.display,
			visibility: section.style.visibility,
			position: section.style.position,
			pointerEvents: section.style.pointerEvents,
			width: section.style.width
		};
		containerStyles = {
			display: container.style.display,
			visibility: container.style.visibility,
			position: container.style.position,
			pointerEvents: container.style.pointerEvents,
			width: container.style.width
		};

		section.style.display = 'block';
		section.style.visibility = 'hidden';
		section.style.position = 'absolute';
		section.style.pointerEvents = 'none';
		section.style.width = '100%';

		container.style.display = 'block';
		container.style.visibility = 'hidden';
		container.style.position = 'relative';
		container.style.pointerEvents = 'none';
		container.style.width = '100%';
	}

	try {
		const figure = await loadFigure(spec.dataKey);
		const layout = applyEconomistTouches(figure.layout || {});
		const data = prepareRegionalTraces(figure.data || [], {
			highlightRegion: spec.highlightRegion,
			hoverFallback: spec.hoverFallback
		});

		const dimensions = computePlotDimensions(container);
		if (dimensions.width > 0 && dimensions.height > 0) {
			layout.width = dimensions.width;
			layout.height = dimensions.height;
			layout.autosize = false;
		}

		const baseConfig = {
			responsive: true,
			displaylogo: false,
			locale: 'es',
			modeBarButtonsToRemove: ['lasso2d', 'select2d']
		};

		await Plotly.newPlot(container, data, layout, {
			...baseConfig,
			...(spec.config || {})
		});

		if (dimensions.width > 0 && dimensions.height > 0) {
			await Plotly.relayout(container, { autosize: true });
		}

		Plotly.Plots.resize(container);
		container.dataset.chartLoaded = 'true';
	} catch (error) {
		console.error(`Error al renderizar ${spec.dataKey}`, error);
		container.innerHTML =
			'<p class="chart-error">No se pudo cargar el gráfico. Verifica que los datos embebidos estén disponibles.</p>';
	} finally {
		if (needsTemporaryReveal && sectionStyles && containerStyles) {
			section.style.display = sectionStyles.display;
			section.style.visibility = sectionStyles.visibility;
			section.style.position = sectionStyles.position;
			section.style.pointerEvents = sectionStyles.pointerEvents;
			section.style.width = sectionStyles.width;

			container.style.display = containerStyles.display;
			container.style.visibility = containerStyles.visibility;
			container.style.position = containerStyles.position;
			container.style.pointerEvents = containerStyles.pointerEvents;
			container.style.width = containerStyles.width;
		}
	}
}

function resizeVisibleCharts() {
	const visibleContainers = document.querySelectorAll('.section.active .chart-container');
	visibleContainers.forEach((container) => {
		if (container.dataset.chartLoaded === 'true') {
			requestAnimationFrame(() => Plotly.Plots.resize(container));
		}
	});
}

function initNavigation() {
	const navLinks = document.querySelectorAll('.nav-link');
	const sections = document.querySelectorAll('.section');

	navLinks.forEach((link) => {
		link.addEventListener('click', () => {
			const targetId = link.getAttribute('data-section');
			navLinks.forEach((item) => item.classList.remove('active'));
			sections.forEach((section) => section.classList.remove('active'));
			link.classList.add('active');
			const targetSection = document.getElementById(targetId);
			if (targetSection) {
				targetSection.classList.add('active');
				resizeVisibleCharts();
			}
		});
	});
}

async function initCharts() {
	await renderChart(FIGURE_SPECS.ventasMensuales);
	renderChart(FIGURE_SPECS.variacionInteranual);
}

document.addEventListener('DOMContentLoaded', async () => {
	initNavigation();
	await initCharts();
	resizeVisibleCharts();
	window.addEventListener('resize', resizeVisibleCharts);
});
