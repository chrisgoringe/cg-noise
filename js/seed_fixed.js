import { app } from "../../../scripts/app.js";

app.registerExtension({
	name: "cg.noise.seedFixed",
	version: 1,
	async nodeCreated(node) {
        if (node.widgets.find((w) => w.name === 'variation_seed')) {
            const cag = node.widgets.find((w) => w.name === 'control_after_generate');
            cag.value = 'fixed'
        }
    }
});