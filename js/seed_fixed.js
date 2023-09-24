import { app } from "../../../scripts/app.js";
import { addValueControlWidget } from "../../../scripts/widgets.js";

app.registerExtension({
	name: "cg.noise.seedFixed",
	version: 1,
	async nodeCreated(node) {
        const variationSeedWidgetIndex = node.widgets?.findIndex((w) => w.name === 'variation_seed');
        if (variationSeedWidgetIndex > -1) {
            const variationSeedWidget = node.widgets[variationSeedWidgetIndex];
            const variationSeedValueControl = addValueControlWidget(node, variationSeedWidget, "fixed");
            //variationSeedWidget.widget.linkedWidgets = [variationSeedValueControl];

            node.widgets.splice(variationSeedWidgetIndex+1,0,node.widgets.pop());

            node.widgets.forEach((w) => { if (w.name === 'control_after_generate') { w.value="fixed"}; });
        }
    }
});