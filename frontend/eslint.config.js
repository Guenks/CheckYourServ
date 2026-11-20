import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import prettier from 'eslint-config-prettier'
import globals from 'globals'

export default [
    { ignores: ['dist/**', 'node_modules/**'] },
    js.configs.recommended,
    ...pluginVue.configs['flat/recommended'],
    prettier,
    {
        languageOptions: { globals: globals.browser },
        rules: {
            'no-unused-vars': 'warn',
            'no-restricted-syntax': [
                'error',
                {
                    selector: 'Identifier[name=/[^\\x00-\\x7F]/]',
                    message: 'Identifiers must be written in English (ASCII only).',
                },
            ],
        },
    },
]