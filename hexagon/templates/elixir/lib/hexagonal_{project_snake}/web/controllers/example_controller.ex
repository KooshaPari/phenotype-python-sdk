defmodule {{ project_module }}Web.ExampleController do
  @moduledoc """
  HTTP controller for example entities.
  """

  use Phoenix.Controller, namespace: {{ project_module }}Web
  alias {{ project_module }}.Application.ExampleService
  alias {{ project_module }}.Adapters.Persistence.InMemoryRepository

  # Service instance initialized with the repository
  @service ExampleService.new(InMemoryRepository)

  def index(conn, _params) do
    case ExampleService.list_examples(@service) do
      {:ok, examples} ->
        json(conn, %{data: examples})

      {:error, reason} ->
        conn
        |> put_status(500)
        |> json(%{error: reason})
    end
  end

  def show(conn, %{"id" => id}) do
    case ExampleService.get_example(@service, id) do
      {:ok, example} ->
        json(conn, %{data: example})

      {:error, :not_found} ->
        conn
        |> put_status(404)
        |> json(%{error: "Example not found"})
    end
  end

  def create(conn, params) do
    %{
      "id" => id,
      "name" => name,
      "description" => description
    } = params

    case ExampleService.create_example(@service, id, name, description) do
      {:ok, example} ->
        conn
        |> put_status(201)
        |> json(%{data: example})

      {:error, :invalid_input} ->
        conn
        |> put_status(400)
        |> json(%{error: "Invalid input"})
    end
  end

  def update(conn, %{"id" => id} = params) do
    attrs = Map.take(params, ["name", "description"])

    case ExampleService.update_example(@service, id, attrs) do
      {:ok, example} ->
        json(conn, %{data: example})

      {:error, :not_found} ->
        conn
        |> put_status(404)
        |> json(%{error: "Example not found"})
    end
  end

  def delete(conn, %{"id" => id}) do
    case ExampleService.delete_example(@service, id) do
      :ok ->
        send_resp(conn, 204, "")

      {:error, :not_found} ->
        conn
        |> put_status(404)
        |> json(%{error: "Example not found"})
    end
  end

  def activate(conn, %{"id" => id}) do
    case ExampleService.activate_example(@service, id) do
      {:ok, example} ->
        json(conn, %{data: example})

      {:error, :not_found} ->
        conn
        |> put_status(404)
        |> json(%{error: "Example not found"})

      {:error, :already_active} ->
        conn
        |> put_status(400)
        |> json(%{error: "Example already active"})
    end
  end

  def complete(conn, %{"id" => id}) do
    case ExampleService.complete_example(@service, id) do
      {:ok, example} ->
        json(conn, %{data: example})

      {:error, :not_found} ->
        conn
        |> put_status(404)
        |> json(%{error: "Example not found"})

      {:error, :not_active} ->
        conn
        |> put_status(400)
        |> json(%{error: "Example must be active first"})
    end
  end

  def archive(conn, %{"id" => id}) do
    case ExampleService.archive_example(@service, id) do
      {:ok, example} ->
        json(conn, %{data: example})

      {:error, :not_found} ->
        conn
        |> put_status(404)
        |> json(%{error: "Example not found"})

      {:error, reason} ->
        conn
        |> put_status(400)
        |> json(%{error: reason})
    end
  end
end
