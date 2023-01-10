
# 8-15 printing models
# using printing_models_functions.py as an import
import printing_models_functions as pmf

unprinted_models = ['phone case', 'dodecahedron', 'robotic hand']
completed_models= []

pmf.printing_models_functions(unprinted_models, completed_models)
pmf.show_completed_models(completed_models)
