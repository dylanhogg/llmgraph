import pkg_resources

package_name = "llmgraph"
version = pkg_resources.get_distribution(package_name).version
prompts_yaml_location = "prompts.yaml"

default_llm_model = "gpt-3.5-turbo"
default_llm_temp = 0.0
default_output_folder = "./_output/"
default_llm_use_localhost = 0
