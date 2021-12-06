const config = {
	mode: 'jit',
	purge: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {
			backgroundImage: {
				char: "url('/image/inventory-sprite.png')"
			},
			backgroundColor: {
				primary: '#7FB3C8',
				secondary: '#283B43',
				accent: '#215567',
				highlight: '#344A53',
				common: 'rgba(163, 141, 109, var(--tw-bg-opacity))',
				magic: 'rgba(138, 138, 255, var(--tw-bg-opacity))',
				rare: 'rgba(255, 255, 117, var(--tw-bg-opacity))',
				unique: 'rgba(177, 98, 37, var(--tw-bg-opacity))'
			},
			colors: {
				common: 'rgba(163, 141, 109, var(--tw-text-opacity))',
				magic: 'rgba(138, 138, 255, var(--tw-text-opacity))',
				rare: 'rgba(255, 255, 117, var(--tw-text-opacity))',
				unique: 'rgba(177, 98, 37, var(--tw-text-opacity))',
				item: 'rgba(138, 138, 255, 1)',
				flavor: 'rgba(177, 98, 37, 1)',
				crafted: 'rgba(179, 179, 255, 1)'
			},
			gridTemplateColumns: {
				'8-custom': 'repeat(8, var(--tw-gc-size))'
			},
			gridTemplateRows: {
				'8-custom': 'repeat(8, var(--tw-gc-size))'
			},
			gridTemplateCellSize: {
				4: '--tw-gc-size: 4rem'
			},
			minWidth: {
				'cell-size': 'var(var(--tw-gc-size))'
			}
		}
	},

	plugins: [],
	corePlugins: {
		ringWidth: false
	}
};

module.exports = config;
