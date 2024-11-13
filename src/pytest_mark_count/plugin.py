#############################################
#	Dual License: BSD-3-Clause AND MPL-2.0	#
#	Copyright (c) 2024, Adam Nogowski		#
#############################################

# Python Includes
import logging
from typing import Any, Final
from enum import StrEnum
from pathlib import Path

# Pytest Includes
import pytest
from pytest import Item
from pytest_metadata.plugin import metadata_key

from _pytest.config import Config
from _pytest.config.argparsing import Parser


def pytest_addoption(parser: Parser):
	group = parser.getgroup('mark-count')
	group.addoption('--mark-count', action='store', dest='count_markers', default=None, help="""Set markers to count (Space Delimited).\nReports marked, unmarked, unique, and total tests.\nex: --marker-count=\"it vt\"""")
	group.addoption('--mark-count-sep', action='store', dest='separate_markers', default=True, help="""Separate markers dict into individual metadata keys\nex: --marker-count-sep=False""")


def pytest_load_initial_conftests(early_config: Config, parser: Parser):
	mark_count_plugin: MarkCountPlugin = MarkCountPlugin(early_config)
	early_config.pluginmanager.register(mark_count_plugin)


class DefaultMarkers(StrEnum):
	TOTAL = "total_found_items"
	MARK = "marked_found_items"
	UNMARK = "unmarked_found_items"
	SINGLE_FOUND_MARK = "single_marked_found_items"
	MULTI_FOUND_MARK = "multi_marked_found_items"
	UNIQUE_SEARCH_MARK = "unique_marked_searched_items"
	SINGLE_SEARCH_MARK = "single_marked_searched_items"
	MULTI_SEARCH_MARK = "multi_marked_searched_items"

	def __repr__(self) -> str:
		return f"{self.value}"


class MarkCountPlugin:

	_search_markers: list[str] | None = None
	_ini_markers: list[str] | None = None
	_markers_count: dict[str, int] = {}

	def __init__(self, config: Config):
		temp_markers: str | None = None
		self.config = config

		for item in DefaultMarkers:
			self._markers_count[item] = 0

		# self._ini_markers = self.config.inicfg.get("markers")
		for key, value in self.config.known_args_namespace._get_kwargs():
			if key == "count_markers":
				temp_markers = value
				break

		if temp_markers is not None and isinstance(temp_markers, str):
			try:
				self._search_markers = temp_markers.split(" ")
				for marker in self._search_markers:
					self._markers_count[marker] = 0
			except:
				logging.error("Please put the marker(s) in a space delimited list")

	@property
	def markers_to_search_for(self) -> list[str] | None:
		return self._search_markers

	@property
	def mark_count_dict(self) -> dict[str, int]:
		return self._markers_count

	def pytest_itemcollected(self, item: Item) -> None:
		self._markers_count[DefaultMarkers.TOTAL] += 1
		item_markers: list[str] = [x.name for x in item.own_markers]

		if len(item_markers) > 0:
			self._markers_count[DefaultMarkers.MARK] += 1
		else:
			self._markers_count[DefaultMarkers.UNMARK] += 1

		if len(item_markers) == 1:
			self._markers_count[DefaultMarkers.SINGLE_FOUND_MARK] += 1
		elif len(item_markers) > 1:
			self._markers_count[DefaultMarkers.MULTI_FOUND_MARK] += 1

		if isinstance(self._search_markers, list) or isinstance(self._search_markers, str):

			intersection: set[str] = set(item_markers) & set(self._search_markers)
			if len(intersection) > 0:
				self._markers_count[DefaultMarkers.UNIQUE_SEARCH_MARK] += 1

			if len(intersection) == 1:
				self._markers_count[DefaultMarkers.SINGLE_SEARCH_MARK] += 1

			elif len(intersection) > 1:
				self._markers_count[DefaultMarkers.MULTI_SEARCH_MARK] += 1

			for name in intersection:
				self._markers_count[name] += 1

	def pytest_report_collectionfinish(self, config: Config, start_path: Path, items: list[Item]) -> str | list[str]:
		self.config.stash[metadata_key]["Searched_Markers"] = self.config.option.count_markers

		if self.config.option.separate_markers:
			for key, value in self._markers_count.items():
				config.stash[metadata_key][key] = value
		else:
			self.config.stash[metadata_key]["Marked_Dict"] = self._markers_count

		return f"Mark-Count: {str(self.mark_count_dict)}"

	def query_markers_count(self, key: str | DefaultMarkers) -> int:
		return self._markers_count[key]
