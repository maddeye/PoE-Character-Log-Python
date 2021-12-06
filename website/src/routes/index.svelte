<script>
	import CharacterList from '$lib/components/CharacterList.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';

	import { getData } from '$lib/stores/fetch';

	const response = getData('http://localhost:5000/api/list');
</script>

{#await $response}
	<div class="spinner">
		<LoadingSpinner />
	</div>
{:then data}
	<CharacterList characters={data} />
{:catch err}
	<p>Error</p>
	<p>{err.message}</p>
{/await}
