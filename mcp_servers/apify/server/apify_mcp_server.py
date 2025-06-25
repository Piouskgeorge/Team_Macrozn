import json
import time
from typing import Any, Dict, List, Optional, Union
from mcp.server.fastmcp import FastMCP
from apify_client import ApifyClient
import asyncio
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Apify client
APIFY_API_KEY = "apify_api_DNKNdXuWP5z1z3t9QPJ9wNdF8mF1tY1WK4B7"
client = ApifyClient(APIFY_API_KEY)

# Create MCP server
mcp = FastMCP("Apify Automation Server")

# =============================================================================
# 🧠 1. ACTORS - Core Agent Work
# =============================================================================

@mcp.tool()
def run_actor(actor_id: str, run_input: Optional[Dict[str, Any]] = None, 
              build: Optional[str] = None, timeout_secs: Optional[int] = None,
              memory_mbytes: Optional[int] = None) -> Dict[str, Any]:
    """
    Run an Apify actor asynchronously.
    
    Args:
        actor_id: Actor ID or username/actor-name
        run_input: Input data for the actor (JSON object)
        build: Tag or number of the actor build to run
        timeout_secs: Timeout for the actor run in seconds
        memory_mbytes: Memory limit for the actor run in megabytes
    
    Returns:
        Dictionary containing run information including run ID and status
    """
    try:
        run = client.actor(actor_id).call(
            run_input=run_input or {},
            build=build,
            timeout_secs=timeout_secs,
            memory_mbytes=memory_mbytes
        )
        return {
            "success": True,
            "run_id": run["id"],
            "status": run["status"],
            "started_at": run["startedAt"],
            "actor_id": run["actId"],
            "default_dataset_id": run["defaultDatasetId"],
            "default_key_value_store_id": run["defaultKeyValueStoreId"]
        }
    except Exception as e:
        logger.error(f"Error running actor {actor_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def run_actor_sync(actor_id: str, run_input: Optional[Dict[str, Any]] = None,
                   build: Optional[str] = None, timeout_secs: Optional[int] = 300,
                   memory_mbytes: Optional[int] = None) -> Dict[str, Any]:
    """
    Run an Apify actor synchronously and return the output.
    
    Args:
        actor_id: Actor ID or username/actor-name
        run_input: Input data for the actor (JSON object)
        build: Tag or number of the actor build to run
        timeout_secs: Timeout for the actor run in seconds (default: 300)
        memory_mbytes: Memory limit for the actor run in megabytes
    
    Returns:
        Dictionary containing run results and output data
    """
    try:
        run = client.actor(actor_id).call(
            run_input=run_input or {},
            build=build,
            timeout_secs=timeout_secs,
            memory_mbytes=memory_mbytes
        )
        
        # Get the output data
        dataset_items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        return {
            "success": True,
            "run_id": run["id"],
            "status": run["status"],
            "finished_at": run["finishedAt"],
            "stats": run["stats"],
            "output": dataset_items,
            "items_count": len(dataset_items)
        }
    except Exception as e:
        logger.error(f"Error running actor sync {actor_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def run_actor_sync_get_dataset(actor_id: str, run_input: Optional[Dict[str, Any]] = None,
                               build: Optional[str] = None, timeout_secs: Optional[int] = 300,
                               limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Run an Apify actor synchronously and return dataset items.
    
    Args:
        actor_id: Actor ID or username/actor-name
        run_input: Input data for the actor (JSON object)
        build: Tag or number of the actor build to run
        timeout_secs: Timeout for the actor run in seconds (default: 300)
        limit: Maximum number of items to return
    
    Returns:
        Dictionary containing dataset items
    """
    try:
        run = client.actor(actor_id).call(
            run_input=run_input or {},
            build=build,
            timeout_secs=timeout_secs
        )
        
        # Get dataset items with optional limit
        dataset_client = client.dataset(run["defaultDatasetId"])
        if limit:
            items = list(dataset_client.iterate_items(limit=limit))
        else:
            items = list(dataset_client.iterate_items())
        
        return {
            "success": True,
            "run_id": run["id"],
            "dataset_id": run["defaultDatasetId"],
            "items": items,
            "items_count": len(items),
            "status": run["status"]
        }
    except Exception as e:
        logger.error(f"Error running actor sync with dataset {actor_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_actor_run(run_id: str) -> Dict[str, Any]:
    """
    Get details of a specific actor run.
    
    Args:
        run_id: ID of the actor run
    
    Returns:
        Dictionary containing run details
    """
    try:
        run = client.run(run_id).get()
        return {
            "success": True,
            "run": run
        }
    except Exception as e:
        logger.error(f"Error getting run {run_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_last_actor_run(actor_id: str) -> Dict[str, Any]:
    """
    Get the last run of a specific actor.
    
    Args:
        actor_id: Actor ID or username/actor-name
    
    Returns:
        Dictionary containing the last run details
    """
    try:
        runs = client.actor(actor_id).runs().list(limit=1)
        if runs.items:
            return {
                "success": True,
                "run": runs.items[0]
            }
        else:
            return {
                "success": False,
                "error": "No runs found for this actor"
            }
    except Exception as e:
        logger.error(f"Error getting last run for actor {actor_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def abort_actor_run(run_id: str) -> Dict[str, Any]:
    """
    Abort a running actor.
    
    Args:
        run_id: ID of the actor run to abort
    
    Returns:
        Dictionary containing abort status
    """
    try:
        result = client.run(run_id).abort()
        return {
            "success": True,
            "message": "Run aborted successfully",
            "run": result
        }
    except Exception as e:
        logger.error(f"Error aborting run {run_id}: {str(e)}")
        return {"success": False, "error": str(e)}

# =============================================================================
# 🎯 2. TASKS - Safer Alternative to Actors
# =============================================================================

@mcp.tool()
def run_task(task_id: str, task_input: Optional[Dict[str, Any]] = None,
             timeout_secs: Optional[int] = None, memory_mbytes: Optional[int] = None) -> Dict[str, Any]:
    """
    Run an Apify task asynchronously.
    
    Args:
        task_id: Task ID or username/task-name
        task_input: Input data for the task (JSON object)
        timeout_secs: Timeout for the task run in seconds
        memory_mbytes: Memory limit for the task run in megabytes
    
    Returns:
        Dictionary containing run information
    """
    try:
        run = client.task(task_id).call(
            task_input=task_input or {},
            timeout_secs=timeout_secs,
            memory_mbytes=memory_mbytes
        )
        return {
            "success": True,
            "run_id": run["id"],
            "status": run["status"],
            "started_at": run["startedAt"],
            "task_id": task_id,
            "default_dataset_id": run["defaultDatasetId"]
        }
    except Exception as e:
        logger.error(f"Error running task {task_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def run_task_sync(task_id: str, task_input: Optional[Dict[str, Any]] = None,
                  timeout_secs: Optional[int] = 300, memory_mbytes: Optional[int] = None) -> Dict[str, Any]:
    """
    Run an Apify task synchronously and return the output.
    
    Args:
        task_id: Task ID or username/task-name
        task_input: Input data for the task (JSON object)
        timeout_secs: Timeout for the task run in seconds (default: 300)
        memory_mbytes: Memory limit for the task run in megabytes
    
    Returns:
        Dictionary containing run results and output data
    """
    try:
        run = client.task(task_id).call(
            task_input=task_input or {},
            timeout_secs=timeout_secs,
            memory_mbytes=memory_mbytes
        )
        
        # Get the output data
        dataset_items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        return {
            "success": True,
            "run_id": run["id"],
            "status": run["status"],
            "finished_at": run["finishedAt"],
            "stats": run["stats"],
            "output": dataset_items,
            "items_count": len(dataset_items)
        }
    except Exception as e:
        logger.error(f"Error running task sync {task_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def run_task_sync_get_dataset(task_id: str, task_input: Optional[Dict[str, Any]] = None,
                              timeout_secs: Optional[int] = 300, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Run an Apify task synchronously and return dataset items.
    
    Args:
        task_id: Task ID or username/task-name
        task_input: Input data for the task (JSON object)
        timeout_secs: Timeout for the task run in seconds (default: 300)
        limit: Maximum number of items to return
    
    Returns:
        Dictionary containing dataset items
    """
    try:
        run = client.task(task_id).call(
            task_input=task_input or {},
            timeout_secs=timeout_secs
        )
        
        # Get dataset items with optional limit
        dataset_client = client.dataset(run["defaultDatasetId"])
        if limit:
            items = list(dataset_client.iterate_items(limit=limit))
        else:
            items = list(dataset_client.iterate_items())
        
        return {
            "success": True,
            "run_id": run["id"],
            "dataset_id": run["defaultDatasetId"],
            "items": items,
            "items_count": len(items),
            "status": run["status"]
        }
    except Exception as e:
        logger.error(f"Error running task sync with dataset {task_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_task(task_id: str) -> Dict[str, Any]:
    """
    Get details of a specific task.
    
    Args:
        task_id: Task ID or username/task-name
    
    Returns:
        Dictionary containing task details
    """
    try:
        task = client.task(task_id).get()
        return {
            "success": True,
            "task": task
        }
    except Exception as e:
        logger.error(f"Error getting task {task_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_last_task_run(task_id: str) -> Dict[str, Any]:
    """
    Get the last run of a specific task.
    
    Args:
        task_id: Task ID or username/task-name
    
    Returns:
        Dictionary containing the last run details
    """
    try:
        runs = client.task(task_id).runs().list(limit=1)
        if runs.items:
            return {
                "success": True,
                "run": runs.items[0]
            }
        else:
            return {
                "success": False,
                "error": "No runs found for this task"
            }
    except Exception as e:
        logger.error(f"Error getting last run for task {task_id}: {str(e)}")
        return {"success": False, "error": str(e)}

# =============================================================================
# 🗃️ 3. DATASETS - Access Outputs
# =============================================================================

@mcp.tool()
def get_datasets(limit: Optional[int] = 10, offset: Optional[int] = 0) -> Dict[str, Any]:
    """
    Get list of datasets.
    
    Args:
        limit: Maximum number of datasets to return (default: 10)
        offset: Number of datasets to skip (default: 0)
    
    Returns:
        Dictionary containing list of datasets
    """
    try:
        datasets = client.datasets().list(limit=limit, offset=offset)
        return {
            "success": True,
            "datasets": datasets.items,
            "total": datasets.total,
            "count": datasets.count,
            "limit": datasets.limit,
            "offset": datasets.offset
        }
    except Exception as e:
        logger.error(f"Error getting datasets: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_dataset(dataset_id: str) -> Dict[str, Any]:
    """
    Get details of a specific dataset.
    
    Args:
        dataset_id: Dataset ID
    
    Returns:
        Dictionary containing dataset details
    """
    try:
        dataset = client.dataset(dataset_id).get()
        return {
            "success": True,
            "dataset": dataset
        }
    except Exception as e:
        logger.error(f"Error getting dataset {dataset_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_dataset_items(dataset_id: str, limit: Optional[int] = None, 
                      offset: Optional[int] = 0, clean: bool = False,
                      format_type: str = "json") -> Dict[str, Any]:
    """
    Get items from a dataset.
    
    Args:
        dataset_id: Dataset ID
        limit: Maximum number of items to return
        offset: Number of items to skip (default: 0)
        clean: Whether to return only non-empty items (default: False)
        format_type: Format of the items - json, csv, xlsx, html, xml, rss (default: json)
    
    Returns:
        Dictionary containing dataset items
    """
    try:
        if limit:
            items = list(client.dataset(dataset_id).iterate_items(
                limit=limit, offset=offset, clean=clean
            ))
        else:
            items = list(client.dataset(dataset_id).iterate_items(
                offset=offset, clean=clean
            ))
        
        return {
            "success": True,
            "dataset_id": dataset_id,
            "items": items,
            "items_count": len(items),
            "format": format_type
        }
    except Exception as e:
        logger.error(f"Error getting items from dataset {dataset_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_dataset_stats(dataset_id: str) -> Dict[str, Any]:
    """
    Get statistics of a dataset.
    
    Args:
        dataset_id: Dataset ID
    
    Returns:
        Dictionary containing dataset statistics
    """
    try:
        dataset = client.dataset(dataset_id).get()
        return {
            "success": True,
            "dataset_id": dataset_id,
            "item_count": dataset.get("itemCount", 0),
            "clean_item_count": dataset.get("cleanItemCount", 0),
            "created_at": dataset.get("createdAt"),
            "modified_at": dataset.get("modifiedAt"),
            "accessed_at": dataset.get("accessedAt")
        }
    except Exception as e:
        logger.error(f"Error getting stats for dataset {dataset_id}: {str(e)}")
        return {"success": False, "error": str(e)}

# =============================================================================
# 📄 4. LOGS - Optional debugging
# =============================================================================

@mcp.tool()
def get_run_log(run_id: str) -> Dict[str, Any]:
    """
    Get log of a specific run.
    
    Args:
        run_id: Run ID
    
    Returns:
        Dictionary containing run log
    """
    try:
        log = client.run(run_id).log().get()
        return {
            "success": True,
            "run_id": run_id,
            "log": log
        }
    except Exception as e:
        logger.error(f"Error getting log for run {run_id}: {str(e)}")
        return {"success": False, "error": str(e)}

# =============================================================================
# 🔑 5. KEY-VALUE STORES - Input/Output Handling
# =============================================================================

@mcp.tool()
def get_key_value_stores(limit: Optional[int] = 10, offset: Optional[int] = 0) -> Dict[str, Any]:
    """
    Get list of key-value stores.
    
    Args:
        limit: Maximum number of stores to return (default: 10)
        offset: Number of stores to skip (default: 0)
    
    Returns:
        Dictionary containing list of key-value stores
    """
    try:
        stores = client.key_value_stores().list(limit=limit, offset=offset)
        return {
            "success": True,
            "stores": stores.items,
            "total": stores.total,
            "count": stores.count,
            "limit": stores.limit,
            "offset": stores.offset
        }
    except Exception as e:
        logger.error(f"Error getting key-value stores: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_key_value_store(store_id: str) -> Dict[str, Any]:
    """
    Get details of a specific key-value store.
    
    Args:
        store_id: Key-value store ID
    
    Returns:
        Dictionary containing store details
    """
    try:
        store = client.key_value_store(store_id).get()
        return {
            "success": True,
            "store": store
        }
    except Exception as e:
        logger.error(f"Error getting key-value store {store_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_key_value_record(store_id: str, key: str) -> Dict[str, Any]:
    """
    Get a record from a key-value store.
    
    Args:
        store_id: Key-value store ID
        key: Record key
    
    Returns:
        Dictionary containing the record value
    """
    try:
        record = client.key_value_store(store_id).get_record(key)
        return {
            "success": True,
            "store_id": store_id,
            "key": key,
            "value": record["value"] if record else None,
            "content_type": record["contentType"] if record else None
        }
    except Exception as e:
        logger.error(f"Error getting record {key} from store {store_id}: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def store_key_value_record(store_id: str, key: str, value: Any, 
                          content_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Store a record in a key-value store.
    
    Args:
        store_id: Key-value store ID
        key: Record key
        value: Record value (can be any JSON-serializable type)
        content_type: Content type of the record (optional)
    
    Returns:
        Dictionary containing operation status
    """
    try:
        client.key_value_store(store_id).set_record(
            key=key,
            value=value,
            content_type=content_type
        )
        return {
            "success": True,
            "store_id": store_id,
            "key": key,
            "message": "Record stored successfully"
        }
    except Exception as e:
        logger.error(f"Error storing record {key} in store {store_id}: {str(e)}")
        return {"success": False, "error": str(e)}

# =============================================================================
# 📋 RESOURCES - Dynamic Access to Actor and Task Information
# =============================================================================

@mcp.resource("actor://{actor_id}")
def get_actor_info(actor_id: str) -> str:
    """Get detailed information about a specific actor"""
    try:
        actor = client.actor(actor_id).get()
        return json.dumps(actor, indent=2)
    except Exception as e:
        return f"Error getting actor {actor_id}: {str(e)}"

@mcp.resource("task://{task_id}")
def get_task_info(task_id: str) -> str:
    """Get detailed information about a specific task"""
    try:
        task = client.task(task_id).get()
        return json.dumps(task, indent=2)
    except Exception as e:
        return f"Error getting task {task_id}: {str(e)}"

@mcp.resource("dataset://{dataset_id}")
def get_dataset_info(dataset_id: str) -> str:
    """Get detailed information about a specific dataset"""
    try:
        dataset = client.dataset(dataset_id).get()
        return json.dumps(dataset, indent=2)
    except Exception as e:
        return f"Error getting dataset {dataset_id}: {str(e)}"

@mcp.resource("run://{run_id}")
def get_run_info(run_id: str) -> str:
    """Get detailed information about a specific run"""
    try:
        run = client.run(run_id).get()
        return json.dumps(run, indent=2)
    except Exception as e:
        return f"Error getting run {run_id}: {str(e)}"

# =============================================================================
# 🚀 UTILITY FUNCTIONS
# =============================================================================

@mcp.tool()
def list_available_actors(
    limit: Optional[int] = 1000,
    offset: Optional[int] = 0,
    my: Optional[bool] = False,
    desc: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    List available actors created or used by the user.
    
    Args:
        limit: Maximum number of actors to return (default: 1000, max: 1000)
        offset: Number of actors to skip (default: 0)
        my: If True, returns only actors owned by the user (default: False)
        desc: If True, sorts actors in descending order (default: False)
    
    Returns:
        Dictionary containing list of available actors
    """
    try:
        # Validate sort_by parameter
        valid_sort_fields = ["createdAt", "lastRunStartedAt"]
        
        # Ensure limit does not exceed 1000
        limit = min(limit, 1000)

        # Map sort_by to API parameter
        sort_param = "createdAt" 

        # Call the Apify API with the appropriate parameters
        actors = client.actors().list(
            limit=limit,
            offset=offset,
            my=my,
            desc=desc,
           
        )

        return {
            "success": True,
            "actors": [
                {
                    "id": actor["id"],
                    "name": actor["name"],
                    "username": actor["username"],
                    "title": actor["title"],
                    "description": actor["description"][:200] + "..." if len(actor.get("description", "")) > 200 else actor.get("description", ""),
                    "runs": actor["stats"]["totalRuns"],
                    "createdAt": actor["createdAt"],
                    "lastRunStartedAt": actor.get("lastRunStartedAt")
                }
                for actor in actors.items
            ],
            "total": actors.total,
            "count": len(actors.items),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error listing actors: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_account_info() -> Dict[str, Any]:
    """
    Get information about the current Apify account.
    
    Returns:
        Dictionary containing account information
    """
    try:
        user = client.user().get()
        return {
            "success": True,
            "user_id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "plan": user["plan"],
            "usage": user.get("usage", {}),
            "limits": user.get("limits", {})
        }
    except Exception as e:
        logger.error(f"Error getting account info: {str(e)}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()