using UnrealBuildTool;

public class StormPlugin : ModuleRules
{
    public StormPlugin(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new string[] { 
            "Core", "CoreUObject", "Engine" 
        });
    }
}