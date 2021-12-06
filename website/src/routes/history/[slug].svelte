<script context="module">
	import { getData } from '$lib/stores/fetch';

	export async function load({ page, fetch }) {
		const { slug } = page.params;

		let history = await getData(`http://localhost:5000/api/history/${slug}`);

		return {
			props: { history }
		};
	}
</script>

<script>
	import CharacterScreen from '$lib/components/CharacterScreen.svelte';
	import HistorySelector from '$lib/components/HistorySelector.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';

	export let history = [];

	let selectedHistory = null;

	const selectTime = ({ detail }) => {
		selectedHistory = detail;
	};
</script>

<div class="wrapper history">
	{#await $history}
		<div class="spinner">
			<LoadingSpinner />
		</div>
	{:then data}
		<div class="history-selector">
			<h1>History:</h1>
			<HistorySelector history={data} on:clicked={selectTime} />
		</div>

		<div class="character-screen">
			<CharacterScreen character={selectedHistory || data[0]} />
		</div>
	{:catch Error}
		<p>Error</p>
	{/await}
</div>

<style>
	.history {
		@apply mt-5;
	}

	.history-selector {
		@apply p-2 bg-highlight rounded-t-md;
	}

	.character-screen {
		@apply mt-0;
	}
</style>
