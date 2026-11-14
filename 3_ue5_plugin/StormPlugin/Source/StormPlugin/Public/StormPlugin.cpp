#include "StormPlugin.h"

#define LOCTEXT_NAMESPACE "FStormPluginModule"

void FStormPluginModule::StartupModule()
{
    // This code will execute after your module is loaded into memory
}

void FStormPluginModule::ShutdownModule()
{
    // This function may be called during shutdown to clean up your module
}

#undef LOCTEXT_NAMESPACE
    
IMPLEMENT_MODULE(FStormPluginModule, StormPlugin)