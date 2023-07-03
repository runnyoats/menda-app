<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	let modalOpen = true; // add this line

	function handleImport() {
		console.log('Import button clicked');
	}

	function handleExport() {
		console.log('Export button clicked');
	}

	function closeModal() {
		dispatch('close');
		modalOpen = false; // update this line
	}
</script>

<div class="modal" class:open={modalOpen}>
	<div class="modal-background" on:click={closeModal} />
	<div class="modal-content">
		<h2 class="text-2xl font-bold mb-10 text-gray-800 text-center">Data Operations</h2>
		<button on:click={handleImport}>Import</button>
		<button on:click={handleExport}>Export</button>
		<button on:click={closeModal}>Close</button>
	</div>
</div>

<!-- Styles omitted for brevity -->

<style>
	.modal {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		visibility: hidden;
		opacity: 0;
		transition: visibility 0s linear 0.25s, opacity 0.25s 0s;
	}

	.modal.open {
		visibility: visible;
		opacity: 1;
		transition: visibility 0s linear 0s, opacity 0.25s 0s;
	}

	.modal-background {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
	}

	.modal-content {
		background: white;
		padding: 1em;
		position: relative;
		z-index: 1;
	}
</style>
